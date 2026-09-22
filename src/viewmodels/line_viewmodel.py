"""LineViewModel: P2P line state — peer list, call state, speed, progress.

A real fax machine has exactly one phone line, and so does this ViewModel:
the states below are mutually exclusive. Discovery feeds peers in via
`set_peers()` (the Control layer wires lanlink's on_change straight here);
transmit/receive transitions are driven by the Control layer's network
bridge in main.py.

Views subscribe via `on_changed` and read state; progress notifications are
time-throttled (~80 ms) so a streaming fax does not hammer page.update().
"""

from __future__ import annotations

import time
from typing import Callable, Optional

# Line states — one call at a time, like a real fax machine.
IDLE = "idle"
DIALING = "dialing"      # outgoing call, waiting for the peer to answer
RINGING = "ringing"      # incoming call, waiting out the ring delay
SENDING = "sending"      # streaming payload out
RECEIVING = "receiving"  # streaming payload in

_STATE_LABELS = {
    IDLE: "Line idle",
    DIALING: "Dialing…",
    RINGING: "Ringing…",
    SENDING: "Sending…",
    RECEIVING: "Receiving…",
}

_PROGRESS_NOTIFY_MIN = 0.08  # seconds between progress-driven refreshes
IDLE_STATUS = "Ready to receive."


class LineViewModel:
    def __init__(self, *, name: str) -> None:
        self.name: str = name
        self.peers: list = []  # lanlink Peer objects
        self.selected_id: Optional[str] = None
        self.state: str = IDLE
        self.status: str = IDLE_STATUS
        self.turbo: bool = False
        self.bytes_done: int = 0
        self.bytes_total: int = 0
        self.row_size: int = 0
        # View subscribes here.
        self.on_changed: Optional[Callable[[], None]] = None
        self._last_notify: float = 0.0

    def _notify(self, *, throttle: bool = False) -> None:
        if throttle:
            now = time.monotonic()
            if now - self._last_notify < _PROGRESS_NOTIFY_MIN:
                return
        self._last_notify = time.monotonic()
        if self.on_changed is not None:
            self.on_changed()

    # ---- derived state (views read, never compute) ----

    @property
    def is_idle(self) -> bool:
        return self.state == IDLE

    @property
    def state_label(self) -> str:
        return _STATE_LABELS.get(self.state, self.state)

    @property
    def progress_label(self) -> str:
        if self.row_size <= 0 or self.bytes_total <= 0:
            return ""
        return f"line {self.lines_done}/{self.lines_total}"

    @property
    def lines_done(self) -> int:
        return self.bytes_done // self.row_size if self.row_size else 0

    @property
    def lines_total(self) -> int:
        return self.bytes_total // self.row_size if self.row_size else 0

    @property
    def selected_peer(self):
        for peer in self.peers:
            if peer.id == self.selected_id:
                return peer
        return None

    # ---- commands ----

    def set_peers(self, peers: list) -> None:
        """Replace the peer table (called by discovery's on_change)."""
        new_sig = [(p.id, p.name, p.host, p.port) for p in peers]
        old_sig = [(p.id, p.name, p.host, p.port) for p in self.peers]
        if new_sig == old_sig:
            return
        self.peers = list(peers)
        if self.selected_id is not None and all(
            p.id != self.selected_id for p in peers
        ):
            self.selected_id = None  # selected peer vanished
        self._notify()

    def select_peer(self, peer_id: Optional[str]) -> None:
        if peer_id == self.selected_id:
            return
        self.selected_id = peer_id
        self._notify()

    def set_state(self, state: str, status: Optional[str] = None) -> None:
        self.state = state
        if state == IDLE:
            self.reset_progress()
            if status is None:
                status = IDLE_STATUS
        if status is not None:
            self.status = status
        self._notify()

    def set_status(self, text: str) -> None:
        self.status = text
        self._notify()

    def set_turbo(self, on: bool) -> None:
        if on == self.turbo:
            return
        self.turbo = on
        self._notify()

    def set_progress(self, done: int, total: int, row_size: int) -> None:
        self.bytes_done = done
        self.bytes_total = total
        self.row_size = row_size
        self._notify(throttle=True)

    def reset_progress(self) -> None:
        self.bytes_done = 0
        self.bytes_total = 0
        self.row_size = 0
