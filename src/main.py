"""Fax machine simulator — full app entry point (Scan + Read + P2P line).

Architecture: Control-View-ViewModel (MVVM)

    src/
    ├── main.py                 # ENTRY: full fax + Control/line wiring
    ├── fax_reader.py           # ENTRY: read-only standalone + Control wiring
    ├── network_protocol.py     # FAX1 codec: FaxDocument <-> lanlink handshake
    ├── lanlink/                # REUSABLE P2P package (stdlib-only, no Flet)
    │   ├── discovery.py        #   multicast/broadcast beacons + peer table
    │   ├── session.py          #   ring/BUSY/paced TCP sessions (Connection,
    │   │                       #   SessionServer, dial)
    │   └── errors.py           #   LineBusy, PeerGone, HandshakeError, ...
    ├── models/
    │   ├── __init__.py
    │   ├── fax_document.py     # FaxDocument dataclass + JSON (de)serialization
    │   ├── scanner.py          # image → 1-bit packed bitmap (BOX avg per cell)
    │   └── receiver.py         # packed bitmap → base64 PNG (+ ProgressiveFax)
    ├── viewmodels/
    │   ├── __init__.py
    │   ├── fax_viewmodel.py    # scan/read state + commands (+ receive path)
    │   ├── line_viewmodel.py   # peers, line state, progress, speed toggle
    │   └── reader_viewmodel.py # read-only state + load command
    └── views/
        ├── __init__.py
        ├── components.py       # ImagePanel, StatusBar, ControlBar, spawn()
        ├── fax_view.py         # build_fax_view: line panel + Scanned | Received
        ├── line_panel.py       # peer picker, Transmit/Hang up, turbo, status
        └── reader_view.py      # build_reader_view: Load + single image

How it works
============

A real fax machine scans a document into a grid of black/white pixels and
transmits them over a phone line; the receiver prints them back onto paper.
This simulator mimics that pipeline in software, replacing the phone line
with a JSON file.

Scanner pipeline (models/scanner.py):

    source image (any size, any format)
        │  PIL Image.open + convert("L")           → grayscale
        ▼
    square grayscale image (center-cropped)
        │  PIL resize((W,H), Resampling.BOX)        → BOX filter averages all
        ▼                                          source pixels in each output
    WxH grid of average grayscale values            cell = exactly the spec's
        │  point(lambda p: 0 if p < threshold else 255, mode="1")
        ▼                                          "average grayscale per cell"
    WxH 1-bit image (mode "1": 0=black, 255=white)
        │  Image.tobytes()                          → packed 1 bit/pixel,
        ▼                                          MSB-first, row-major
    packed bitmap bytes
        │  base64.b64encode(...)                    → ASCII-safe for JSON
        ▼
    FaxDocument JSON: {"version":1,"width":W,"height":H,
                       "threshold":T,"invert":B,"data":"<base64>"}

Threshold direction: darker-than-threshold → black (conventional). The Invert
switch flips the comparison so bright pixels become black instead. Default
threshold = 128. Supported resolutions: 64 / 128 / 256 / 512 / 1024
(all widths are multiples of 8 so the packed bitmap has no row padding).

Receiver pipeline (models/receiver.py):

    JSON text
        │  json.loads + base64.b64decode            → packed bitmap bytes
        ▼
    Image.frombytes("1", (W,H), data)               → reconstructs the exact
        │                                          picture the scanner packed
        ▼
    PIL Image (mode "1", 0=black, 255=white)
        │  save(BytesIO, format="PNG") + base64     → single PNG string
        ▼
    ft.Image(src=base64_png)                         → ONE control renders the
                                                   entire image at any size.

Key design choice: never create one Flet control per pixel. A 1024x1024 fax
would mean ~1M Container widgets and freeze the UI. Instead, the whole fax is
decoded into one PIL Image and displayed via a single ft.Image control.

P2P line (Phase 1: LAN only; lanlink/ is stdlib-only and extraction-ready):

    every instance                                   sender            receiver
        │  Discovery: JSON beacon every 3 s            │                 │
        │  (multicast default-if + loopback,           │                 │
        │   broadcast fallback) on UDP 47555           │                 │
        ▼                                              │                 │
    peer table (id, name, host, tcp_port, last_seen)    │                 │
        │  user picks a peer, clicks Transmit          │                 │
        │                                              │  TCP connect ──▶│
        │                                              │  FAX1 handshake │
        │                                              │     busy? ──▶ BUSY + close
        │                                              │◀── ring delay (2 rings)
        │                                              │◀── ok           │
        │  status: RINGING… (waiting for the answer)   │                 │
        │                                              │  payload rows ─▶│
        │  paced at ~4 s/page (or Turbo = full speed)  │  ProgressiveFax │
        │                                              │◀── ok {bytes}   │  line-by-line
        ▼                                              ▼                 ▼  preview (~40 ms)
    LineViewModel: IDLE/DIALING/RINGING/SENDING/RECEIVING (+ BUSY, hang-up)

Single line like a real fax: SessionServer.is_busy() answers BUSY whenever
the line state is not IDLE, and Hang up cancels the active call task.
Row framing follows the scanner invariant: row size = width // 8 bytes.

MVVM data flow:

    User clicks button
        │  Control layer (this file): async handler runs FilePicker/Camera
        ▼
    FilePicker / Camera returns bytes or path
        │  ViewModel.on_source_selected / load_fax_from_text
        ▼
    Model layer runs scan() or render_png_b64()
        │  ViewModel updates its state fields, calls _notify()
        ▼
    View's on_changed callback fires
        │  reads VM state, updates ImagePanel/StatusBar controls, page.update()
        ▼
    User sees updated Scanned preview | Received image

Re-preview on parameter change: when the user drags the threshold slider or
toggles Invert after a scan, the ViewModel re-runs scan_from_bytes() on the
cached source bytes (no disk re-read). This makes the threshold slider feel
live. Resolution changes also trigger a re-scan because the cell grid changes.

Run:
    uv run flet run            # desktop
    uv run flet run --web      # web
    uv run flet run src/fax_reader.py   # reader only
"""

from __future__ import annotations

import asyncio
import logging
import os

import flet as ft

import network_protocol
from lanlink import (
    Discovery,
    HandshakeError,
    LineBusy,
    PeerGone,
    SessionServer,
    TransferAborted,
    dial,
)
from viewmodels import (
    DIALING,
    IDLE,
    RECEIVING,
    RINGING,
    SENDING,
    FaxViewModel,
    LineViewModel,
)
from views import build_fax_view
from views.components import spawn

_log = logging.getLogger(__name__)

# Simulated phone-line behavior
RING_SECONDS = 0.9       # one audible "ring" on the receiver
RINGS_BEFORE_ANSWER = 2  # auto-answer after this many rings
PAGE_SECONDS = 4.0       # Normal speed: one page takes about this long
MIN_BYTES_PER_SEC = 64   # keeps tiny pages from zipping by at full tick rate


async def main(page: ft.Page) -> None:
    page.title = "Fax Machine"
    page.padding = 16
    page.bgcolor = ft.Colors.GREY_900
    page.theme_mode = ft.ThemeMode.DARK

    vm = FaxViewModel()
    # Unique default name per process so two instances on one machine differ.
    line_vm = LineViewModel(name=f"Fax-{os.getpid()}")

    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    # ---- Control-layer async handlers (bridge FilePicker/Camera -> VM) ----

    async def on_scan() -> None:
        try:
            files = await file_picker.pick_files(
                dialog_title="Pick an image to scan",
                file_type=ft.FilePickerFileType.IMAGE,
                allow_multiple=False,
                with_data=True,
            )
        except Exception as ex:
            vm.set_status(f"File picker failed: {type(ex).__name__}: {ex}")
            return
        if not files:
            vm.set_status("Load cancelled.")
            return
        f = files[0]
        if f.bytes:
            vm.on_source_selected(image_bytes=f.bytes, image_path=f.name)
        elif f.path:
            vm.on_source_selected(image_path=f.path)
        else:
            vm.set_status("Scan failed: no file data.")

    async def on_scan_run() -> None:
        # Process the already-loaded source image into a fax.
        vm.scan()

    async def on_save() -> None:
        json_text = vm.export_json()
        if json_text is None:
            return
        src_bytes = json_text.encode("utf-8")
        try:
            path = await file_picker.save_file(
                dialog_title="Save fax as JSON",
                file_name="fax.json",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["json"],
                src_bytes=src_bytes,
            )
        except Exception as ex:
            vm.set_status(f"File picker failed: {ex}")
            return
        if not path:
            vm.set_status("Save cancelled.")
            return
        # src_bytes passed above makes Flet write the file itself on desktop
        # and download it on web, so there is nothing to write here.
        vm.set_status(f"Saved to {path}")

    async def on_load() -> None:
        try:
            files = await file_picker.pick_files(
                dialog_title="Pick a fax JSON file",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["json"],
                allow_multiple=False,
                with_data=True,
            )
        except Exception as ex:
            vm.set_status(f"File picker failed: {ex}")
            return
        if not files:
            vm.set_status("Load cancelled.")
            return
        f = files[0]
        if f.bytes:
            try:
                vm.load_fax_from_text(f.bytes.decode("utf-8", errors="replace"))
            except Exception as ex:
                vm.set_status(f"Load failed: {ex}")
        elif f.path:
            try:
                with open(f.path, "r", encoding="utf-8") as fh:
                    vm.load_fax_from_text(fh.read())
            except OSError as ex:
                vm.set_status(f"Load failed: {ex}")
        else:
            vm.set_status("Load failed: no file data.")

    # ---- Camera ----
    # Camera MUST be in the visual tree (Stack in page controls) to work on web.
    import flet_camera as fc

    _camera: fc.Camera | None = None
    _camera_ready = False

    # Camera preview area
    _camera_stack = ft.Stack(controls=[], height=320)

    _capture_btn = ft.FilledButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.PHOTO_CAMERA, size=18), ft.Text("Capture")],
            spacing=8,
        ),
        on_click=lambda e: spawn(_on_camera_do_capture),
    )
    _cancel_btn = ft.Button(
        content=ft.Row(
            [ft.Icon(ft.Icons.CLOSE, size=18), ft.Text("Cancel")],
            spacing=8,
        ),
        on_click=lambda e: _on_camera_cancel(),
    )
    _retake_btn = ft.FilledButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.REFRESH, size=18), ft.Text("Retake")],
            spacing=8,
        ),
        on_click=lambda e: spawn(_on_camera_retake),
    )
    _done_btn = ft.Button(
        content=ft.Row(
            [ft.Icon(ft.Icons.CHECK, size=18), ft.Text("Done")],
            spacing=8,
        ),
        on_click=lambda e: _on_camera_cancel(),
    )

    # Two button rows: capture/cancel (during preview) and retake/done (after capture)
    _camera_btns_capture = ft.Row(
        controls=[_capture_btn, _cancel_btn],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
    )
    _camera_btns_retake = ft.Row(
        controls=[_retake_btn, _done_btn],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
        visible=False,
    )
    _camera_area = ft.Column(
        controls=[_camera_stack, _camera_btns_capture, _camera_btns_retake],
        spacing=8,
        visible=False,
        expand=False,
    )

    def _create_camera() -> fc.Camera:
        return fc.Camera(
            expand=True,
            preview_enabled=True,
            content=ft.Container(
                alignment=ft.Alignment.CENTER,
                content=ft.Icon(
                    ft.Icons.CENTER_FOCUS_STRONG,
                    color=ft.Colors.WHITE_70,
                    size=48,
                ),
            ),
        )

    async def _init_camera() -> bool:
        """Create a fresh Camera, mount it, and initialize it."""
        nonlocal _camera_ready, _camera
        # Tear down old camera
        _camera_stack.controls.clear()
        _camera = None
        _camera_ready = False
        # Create fresh camera
        _camera = _create_camera()
        _camera_stack.controls.append(_camera)
        _camera_area.visible = True
        _camera_area.update()
        await asyncio.sleep(0.3)
        devices: list[fc.CameraDescription] = []
        try:
            devices = await _camera.get_available_cameras()
        except Exception:
            pass
        init_kwargs = dict(
            resolution_preset=fc.ResolutionPreset.MEDIUM,
            enable_audio=False,
            image_format_group=fc.ImageFormatGroup.JPEG,
        )
        try:
            if devices:
                await _camera.initialize(description=devices[0], **init_kwargs)
            else:
                await _camera.initialize(**init_kwargs)
        except Exception as ex:
            vm.set_status(f"Camera init failed: {ex}")
            _hide_camera_area()
            return False
        _camera_ready = True
        return True

    def _hide_camera_area() -> None:
        _camera_area.visible = False
        _camera_area.update()

    def _show_camera_area() -> None:
        _camera_area.visible = True
        _camera_area.update()

    def _on_camera_cancel() -> None:
        _hide_camera_area()
        vm.set_status("Camera cancelled.")
        page.update()

    async def _on_camera_do_capture() -> None:
        if _camera is None:
            return
        try:
            data = await _camera.take_picture()
        except Exception as ex:
            vm.set_status(f"Camera capture failed: {ex}")
            return
        if not data:
            vm.set_status("Camera capture returned no data.")
            return
        # Send directly to ViewModel — shows in Original tab
        vm.on_source_selected(image_bytes=data, image_path="(camera)")
        # Switch buttons: hide capture/cancel, show retake/done
        _camera_btns_capture.visible = False
        _camera_btns_retake.visible = True
        _camera_area.update()

    async def _on_camera_retake() -> None:
        # Camera is still active — just switch buttons back to capture mode
        _camera_btns_retake.visible = False
        _camera_btns_capture.visible = True
        _camera_area.update()

    async def _open_camera_preview() -> None:
        ready = await _init_camera()
        if not ready:
            vm.set_status("Camera is not available on this platform.")
            return
        _camera_btns_retake.visible = False
        _camera_btns_capture.visible = True
        _show_camera_area()
        vm.set_status("Camera ready — frame and capture.")
        page.update()

    async def on_camera_button() -> None:
        await _open_camera_preview()

    extra_buttons: list = []
    extra_buttons.append(
        ft.FilledButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.PHOTO_CAMERA, size=18), ft.Text("Camera")],
                spacing=8,
            ),
            on_click=lambda e: spawn(on_camera_button),
        )
    )

    # ---- P2P line: network wiring (Control layer bridges lanlink -> VMs) ----

    _discovery: Discovery | None = None
    _server: SessionServer | None = None
    _send_task: asyncio.Task | None = None  # the active outgoing call

    def _line_busy() -> bool:
        # One line per machine: any non-IDLE state answers BUSY to new calls.
        return not line_vm.is_idle

    def _on_ringing(header: dict) -> None:
        sender = str(header.get("sender") or "a peer")
        line_vm.set_state(RINGING, status=f"Incoming call from {sender}…")

    def _validate(header: dict) -> None:
        network_protocol.parse_handshake(header)  # raises HandshakeError

    async def _on_incoming(header: dict, conn) -> int:
        """Runs inside the SessionServer call task: feed rows into the VM as
        they land on the wire so the received page fills line by line live."""
        sender, meta = network_protocol.parse_handshake(header)
        vm.begin_receive(meta, sender=sender)
        line_vm.set_state(RECEIVING, status=f"Receiving from {sender}…")
        rs = network_protocol.row_size(meta["width"])
        total = meta["bytes"]
        buf = bytearray()
        rows_fed = 0
        try:
            async for chunk in conn.iter_payload(total):
                buf.extend(chunk)
                line_vm.set_progress(len(buf), total, rs)
                # Hand every complete row to the VM the moment it arrives.
                while len(buf) >= (rows_fed + 1) * rs:
                    off = rows_fed * rs
                    vm.receive_row(bytes(buf[off : off + rs]))
                    rows_fed += 1
        except asyncio.CancelledError:
            vm.abort_receive("Receive cancelled — line hung up.")
            line_vm.set_state(IDLE, status="Hung up during receive.")
            raise
        except (TransferAborted, OSError) as ex:
            vm.abort_receive(f"Receive failed: {ex}")
            line_vm.set_state(IDLE, status=f"Receive failed: {ex}")
            return  # connection is broken; the server's finally closes it
        vm.finish_receive(sender=sender)
        line_vm.set_state(
            IDLE, status=f"Received {meta['width']}x{meta['height']} from {sender}."
        )
        return total

    async def _start_network() -> None:
        nonlocal _discovery, _server
        try:
            _server = SessionServer(
                is_busy=_line_busy,
                on_incoming=_on_incoming,
                accept_delay=RING_SECONDS * RINGS_BEFORE_ANSWER,
                on_ringing=_on_ringing,
                validate=_validate,
                on_error=lambda ex: _log.warning("incoming call failed: %s", ex),
            )
            tcp_port = await _server.start()
            _discovery = Discovery(
                name=line_vm.name,
                tcp_port=tcp_port,
                on_change=line_vm.set_peers,
            )
            await _discovery.start()
            line_vm.set_status(
                f"{line_vm.name} is online — select a peer to transmit."
            )
        except OSError as ex:
            line_vm.set_status(f"Network unavailable: {ex}")
            _log.warning("network start failed", exc_info=ex)

    async def on_transmit() -> None:
        """Dial the selected peer and stream the scanned fax out."""
        nonlocal _send_task
        doc = vm.current_fax
        peer = line_vm.selected_peer
        if doc is None:
            line_vm.set_status("Scan a document before transmitting.")
            return
        if peer is None:
            line_vm.set_status("Select a peer first.")
            return
        if not line_vm.is_idle:
            line_vm.set_status("Line is busy — hang up first.")
            return
        _send_task = asyncio.current_task()
        rs = network_protocol.row_size(doc.width)
        total = len(doc.data)
        handshake = network_protocol.build_handshake(doc, sender=line_vm.name)
        line_vm.set_state(DIALING, status=f"Dialing {peer.name}…")
        conn = None
        try:
            conn = await dial(
                peer.host,
                peer.port,
                handshake,
                on_waiting=lambda: line_vm.set_status(f"Ringing {peer.name}…"),
            )
            line_vm.set_state(SENDING, status=f"Sending to {peer.name}…")
            bps = None if line_vm.turbo else max(int(total / PAGE_SECONDS), MIN_BYTES_PER_SEC)
            await conn.send_payload(
                doc.data,
                bytes_per_second=bps,
                on_progress=lambda done, tot: line_vm.set_progress(done, tot, rs),
            )
            reply = await conn.recv_json()
            if reply.get("reply") != "ok" or reply.get("bytes") != total:
                raise TransferAborted(f"receiver reported {reply!r}")
        except asyncio.CancelledError:
            line_vm.set_state(IDLE, status="Hung up.")
            vm.set_status("Transmission cancelled.")
            raise
        except LineBusy:
            line_vm.set_state(IDLE, status=f"{peer.name} is busy — line in use.")
        except (PeerGone, HandshakeError, TransferAborted, OSError, asyncio.TimeoutError) as ex:
            line_vm.set_state(IDLE, status=f"Call failed: {ex}")
        else:
            line_vm.set_state(IDLE, status=f"Sent {doc.width}x{doc.height} to {peer.name}.")
            vm.set_status(f"Sent {doc.width}x{doc.height} to {peer.name}.")
        finally:
            # Close on every path — including cancellation — so the receiver
            # sees the hang-up instead of waiting on a half-open socket.
            if conn is not None:
                try:
                    await conn.close()
                except Exception:
                    pass
            _send_task = None

    async def on_hangup() -> None:
        """Cancel the active call on either side of the line."""
        if line_vm.is_idle:
            return
        if _send_task is not None:
            _send_task.cancel()
        if _server is not None:
            _server.cancel_active()
        line_vm.set_state(IDLE, status="Hung up.")

    # ---- Build view and add to page ----
    view = build_fax_view(
        page,
        vm,
        on_scan=on_scan,
        on_scan_run=on_scan_run,
        on_save=on_save,
        on_load=on_load,
        extra_buttons=extra_buttons or None,
        line_vm=line_vm,
        on_transmit=on_transmit,
        on_hangup=on_hangup,
    )

    # Discovery + listener run in the background for the page's lifetime.
    spawn(_start_network)

    # Camera stack sits below the main view — invisible until user clicks Camera
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[_camera_area, view],
                expand=True,
                spacing=0,
            ),
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
