"""Peer discovery: multicast/broadcast beacons plus an expiring peer table.

Every lanlink endpoint periodically announces itself with a small JSON beacon
and listens for announcements from others. The peer table is pruned when
beacons stop (a peer that leaves without saying goodbye disappears after
`PEER_EXPIRY` seconds).

Transport notes (spike-verified on Linux):

* Plain UDP broadcast does NOT fan out to multiple sockets bound to the same
  port on one host on some machines, so multicast is the primary transport.
* The socket joins the multicast group on every useful interface (default +
  loopback); each beacon is emitted up to three ways:
    1. multicast via the default interface  -> other machines on the LAN
    2. multicast via loopback               -> other instances on this host
    3. limited broadcast                    -> access points that filter
       multicast but forward broadcast.
* Discovery broadcasts are only listened to here; peers are keyed by their
  stable `id` so duplicate beacon paths refresh `last_seen` instead of
  duplicating entries.

Stdlib-only: no Flet, no application imports. Extraction-ready.
"""

from __future__ import annotations

import asyncio
import json
import logging
import socket
import time
import uuid
from dataclasses import dataclass
from typing import Callable, Optional

BEACON_PORT = 47555
MCAST_GRP = "239.255.42.99"
BEACON_INTERVAL = 3.0
PEER_EXPIRY = 12.0
PROTOCOL_VERSION = 1

_log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Peer:
    """A discovered lanlink endpoint.

    `host` is filled from the beacon's source address today (LAN phase);
    Phase 2 can route through a relay instead without changing consumers.
    """

    id: str
    name: str
    host: str
    port: int
    last_seen: float


class _BeaconProtocol(asyncio.DatagramProtocol):
    def __init__(self, owner: "Discovery") -> None:
        self._owner = owner

    def datagram_received(self, data: bytes, addr) -> None:
        self._owner._handle_beacon(data, addr)

    def error_received(self, exc: Exception) -> None:
        _log.debug("discovery socket error: %s", exc)


class Discovery:
    """Announce this endpoint and track other lanlink peers on the network."""

    def __init__(
        self,
        *,
        name: str,
        tcp_port: int,
        on_change: Callable[[list[Peer]], None],
        peer_id: Optional[str] = None,
        service: str = "lanlink",
        beacon_port: int = BEACON_PORT,
    ) -> None:
        self._id = peer_id or uuid.uuid4().hex
        self._name = name
        self._tcp_port = tcp_port
        self._service = service
        self._beacon_port = beacon_port
        self._on_change = on_change
        self._peers: dict[str, Peer] = {}
        self._transport: Optional[asyncio.DatagramTransport] = None
        self._tasks: list[asyncio.Task] = []
        self._started = False

    @property
    def peer_id(self) -> str:
        return self._id

    @property
    def started(self) -> bool:
        return self._started

    def peers(self) -> list[Peer]:
        """Known peers, sorted by display name."""
        return sorted(self._peers.values(), key=lambda p: p.name.lower())

    def get(self, peer_id: str) -> Optional[Peer]:
        return self._peers.get(peer_id)

    async def start(self) -> None:
        if self._started:
            return
        loop = asyncio.get_running_loop()
        transport, _ = await loop.create_datagram_endpoint(
            lambda: _BeaconProtocol(self),
            sock=self._make_socket(),
        )
        self._transport = transport
        self._started = True
        self._tasks = [
            asyncio.create_task(self._beacon_loop(), name="lanlink-beacon"),
            asyncio.create_task(self._prune_loop(), name="lanlink-prune"),
        ]

    async def stop(self) -> None:
        for task in self._tasks:
            task.cancel()
        for task in self._tasks:
            try:
                await task
            except asyncio.CancelledError:
                pass
        self._tasks = []
        if self._transport is not None:
            self._transport.close()
            self._transport = None
        self._started = False
        self._peers.clear()

    # ---- internals ----

    def _make_socket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        for attr in ("SO_REUSEPORT",):  # allow several instances on one host
            opt = getattr(socket, attr, None)
            if opt is not None:
                try:
                    sock.setsockopt(socket.SOL_SOCKET, opt, 1)
                except OSError:
                    pass
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("", self._beacon_port))
        for iface in ("0.0.0.0", "127.0.0.1"):
            mreq = socket.inet_aton(MCAST_GRP) + socket.inet_aton(iface)
            try:
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            except OSError as ex:
                _log.debug("multicast join on %s failed: %s", iface, ex)
        return sock

    def _beacon_payload(self) -> bytes:
        return json.dumps(
            {
                "v": PROTOCOL_VERSION,
                "svc": self._service,
                "id": self._id,
                "name": self._name,
                "tcp_port": self._tcp_port,
            },
            ensure_ascii=True,
        ).encode("utf-8")

    def _send_beacon(self) -> None:
        if self._transport is None:
            return
        data = self._beacon_payload()
        # 1. multicast via default interface (other machines on the LAN)
        self._send_to(data, (MCAST_GRP, self._beacon_port))
        # 2. multicast via loopback (other instances on this host)
        try:
            self._transport.get_extra_info("socket").setsockopt(
                socket.IPPROTO_IP,
                socket.IP_MULTICAST_IF,
                socket.inet_aton("127.0.0.1"),
            )
            self._send_to(data, (MCAST_GRP, self._beacon_port))
            self._transport.get_extra_info("socket").setsockopt(
                socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton("0.0.0.0")
            )
        except OSError as ex:
            _log.debug("loopback multicast send failed: %s", ex)
        # 3. limited broadcast (APs that drop multicast)
        self._send_to(data, ("255.255.255.255", self._beacon_port))

    def _send_to(self, data: bytes, addr: tuple[str, int]) -> None:
        try:
            self._transport.sendto(data, addr)  # type: ignore[union-attr]
        except OSError as ex:
            _log.debug("beacon send to %s failed: %s", addr, ex)

    async def _beacon_loop(self) -> None:
        while True:
            self._send_beacon()
            await asyncio.sleep(BEACON_INTERVAL)

    async def _prune_loop(self) -> None:
        while True:
            await asyncio.sleep(BEACON_INTERVAL)
            now = time.time()
            stale = [
                pid
                for pid, peer in self._peers.items()
                if now - peer.last_seen > PEER_EXPIRY
            ]
            if stale:
                for pid in stale:
                    del self._peers[pid]
                self._notify()

    def _handle_beacon(self, data: bytes, addr) -> None:
        try:
            obj = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return
        if not isinstance(obj, dict):
            return
        if obj.get("v") != PROTOCOL_VERSION or obj.get("svc") != self._service:
            return
        pid = obj.get("id")
        name = obj.get("name")
        port = obj.get("tcp_port")
        if not isinstance(pid, str) or not pid or not isinstance(name, str):
            return
        if not isinstance(port, int) or not (0 < port < 65536):
            return
        if pid == self._id:  # our own beacon looping back
            return
        host = addr[0]
        prev = self._peers.get(pid)
        if prev is not None:
            changed = prev.host != host or prev.port != port or prev.name != name
            self._peers[pid] = Peer(pid, name, host, port, time.time())
            if not changed:
                return  # routine refresh: table view does not need re-render
        else:
            self._peers[pid] = Peer(pid, name, host, port, time.time())
        self._notify()

    def _notify(self) -> None:
        try:
            self._on_change(self.peers())
        except Exception:
            _log.exception("discovery on_change callback failed")
