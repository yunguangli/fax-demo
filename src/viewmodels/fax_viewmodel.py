"""FaxViewModel: full scan + read state and commands.

State is mutated only by the command methods, each of which calls `_notify()`
at the end so the View can refresh. The Control layer (main.py) wires the
async FilePicker/Camera results into `on_source_selected` and `load_fax_*`.

Re-preview behavior: when a scan exists and the user adjusts resolution /
threshold / invert, we re-run the scan from the cached source bytes (no disk
re-read). Resolution changes require a fresh scan because the cell grid
changes; threshold/invert only need a re-binarize but the cheapest path is
to re-scan from the cached bytes anyway.
"""

from __future__ import annotations

import time
from typing import Callable, Optional

from models import (
    DEFAULT_INVERT,
    DEFAULT_RESOLUTION,
    DEFAULT_THRESHOLD,
    FaxDocument,
    ProgressiveFax,
    image_to_png_b64,
    original_png_b64,
    render_png_b64,
    scan_stages_from_bytes,
)

# Progressive-receive render cadence: how often the partial image is
# re-encoded while rows stream in (~25 fps — fast enough that the page
# visibly fills line by line instead of popping in at the end).
_RENDER_INTERVAL = 0.04


class FaxViewModel:
    def __init__(self) -> None:
        # Scanner parameters
        self.resolution: int = DEFAULT_RESOLUTION
        self.threshold: int = DEFAULT_THRESHOLD
        self.invert: bool = DEFAULT_INVERT

        # Cached source image bytes (from FilePicker or Camera)
        self._source_bytes: Optional[bytes] = None
        self.source_path: str = ""

        # Scan results
        self.current_fax: Optional[FaxDocument] = None
        self.original_b64: Optional[str] = None  # source image preview (tab 1)
        self.grayscale_b64: Optional[str] = None  # grayscale preview (tab 2)
        self.scanned_preview_b64: Optional[str] = None  # rendered scan preview (tab 3)
        self.received_b64: Optional[str] = None  # rendered received image

        # Whether a scan has actually been run (so slider re-preview only
        # fires after an explicit scan, not merely after picking a source).
        self._has_scanned: bool = False

        # Progressive receive (network path)
        self._incoming: Optional[ProgressiveFax] = None
        self._incoming_sender: str = ""
        self._incoming_last_render: float = 0.0

        # Status
        self.status: str = "Load or capture an image, then tap Scan."
        self.payload_size: int = 0
        self.dimensions: str = ""

        # View subscribes here.
        self.on_changed: Optional[Callable[[], None]] = None

    def _notify(self) -> None:
        if self.on_changed is not None:
            self.on_changed()

    def set_status(self, text: str) -> None:
        """Allow the Control layer to report FilePicker/Camera outcomes."""
        self.status = text
        self._notify()

    # ---- parameter setters (re-preview if a scan exists) ----

    def set_resolution(self, value: int) -> None:
        if value == self.resolution:
            return
        self.resolution = value
        if self._has_scanned:
            self._rescan()
        else:
            self._notify()

    def set_threshold(self, value: int) -> None:
        if value == self.threshold:
            return
        self.threshold = value
        if self._has_scanned:
            self._rescan()
        else:
            self._notify()

    def set_invert(self, value: bool) -> None:
        if value == self.invert:
            return
        self.invert = value
        if self._has_scanned:
            self._rescan()
        else:
            self._notify()

    # ---- scan commands ----

    def on_source_selected(
        self,
        *,
        image_bytes: Optional[bytes] = None,
        image_path: Optional[str] = None,
    ) -> None:
        """Called by the Control layer with FilePicker/Camera results.

        Stores the source and shows its preview in tab 1; it does NOT run the
        scan. A separate `scan()` call processes it. Picking a new source
        erases any previously scanned/previewed images.
        """
        try:
            if image_bytes is not None:
                self._source_bytes = image_bytes
                self.source_path = "(camera capture)" if image_path is None else image_path
            elif image_path is not None:
                with open(image_path, "rb") as f:
                    self._source_bytes = f.read()
                self.source_path = image_path
            else:
                return
            self._has_scanned = False
            self.original_b64 = original_png_b64(self._source_bytes)
            self.grayscale_b64 = None
            self.scanned_preview_b64 = None
            self.received_b64 = None
            self.current_fax = None
            self.payload_size = 0
            self.dimensions = ""
            self.status = f"Loaded {self.source_path}. Tap Scan to process."
            self._notify()
        except Exception as ex:
            self.status = f"Load failed: {ex}"
            self._notify()

    def scan(self) -> None:
        """Process the loaded source image into a fax (runs the scan pipeline)."""
        if self._source_bytes is None:
            self.status = "Load or capture an image first."
            self._notify()
            return
        self._rescan()
        if self.current_fax is not None:
            self._has_scanned = True

    def _rescan(self) -> None:
        """Re-run the scan from cached source bytes with current parameters."""
        if self._source_bytes is None:
            return
        try:
            stages = scan_stages_from_bytes(
                self._source_bytes,
                resolution=self.resolution,
                threshold=self.threshold,
                invert=self.invert,
            )
        except Exception as ex:
            self.status = f"Scan failed: {ex}"
            self._notify()
            return
        doc = stages.document
        self.current_fax = doc
        self.original_b64 = original_png_b64(self._source_bytes)
        self.grayscale_b64 = image_to_png_b64(stages.grayscale)
        self.scanned_preview_b64 = render_png_b64(doc)
        # In the full fax app, "received" mirrors "scanned" so the user can
        # see the round-trip in real time.
        self.received_b64 = self.scanned_preview_b64
        self.payload_size = doc.payload_size
        self.dimensions = f"{doc.width}x{doc.height}"
        self.status = f"Scanned {self.dimensions} ({doc.payload_size} B payload)."
        self._notify()

    # ---- JSON save/load ----

    def export_json(self) -> Optional[str]:
        """Return the current fax as a JSON string, or None if nothing scanned."""
        if self.current_fax is None:
            self.status = "Nothing to export — scan an image first."
            self._notify()
            return None
        return self.current_fax.to_json()

    def load_fax_from_text(self, json_text: str) -> None:
        """Load a fax from JSON text; updates the 'received' preview."""
        try:
            doc = FaxDocument.from_json(json_text)
        except Exception as ex:
            self.status = f"Load failed: {ex}"
            self._notify()
            return
        self.current_fax = doc
        self.received_b64 = render_png_b64(doc)
        # Keep the Scanned (preview) tab in sync with the loaded fax.
        self.scanned_preview_b64 = self.received_b64
        self.payload_size = doc.payload_size
        self.dimensions = f"{doc.width}x{doc.height}"
        # Sync parameters from the loaded document so the controls reflect it.
        self.resolution = doc.width
        self.threshold = doc.threshold
        self.invert = doc.invert
        self.status = f"Loaded fax {self.dimensions} ({doc.payload_size} B)."
        self._notify()

    def clear(self) -> None:
        self._source_bytes = None
        self.source_path = ""
        self.current_fax = None
        self.original_b64 = None
        self.grayscale_b64 = None
        self.scanned_preview_b64 = None
        self.received_b64 = None
        self.payload_size = 0
        self.dimensions = ""
        self._has_scanned = False
        self._incoming = None
        self.status = "Cleared."
        self._notify()

    # ---- P2P receive (bridged from the network layer in main.py) ----

    @property
    def is_receiving(self) -> bool:
        return self._incoming is not None

    def begin_receive(self, meta: dict, *, sender: str) -> None:
        """Start a progressive receive; the incoming dims adopt immediately."""
        self._incoming = ProgressiveFax(
            meta["width"],
            meta["height"],
            threshold=meta["threshold"],
            invert=meta["invert"],
        )
        self._incoming_sender = sender
        self._incoming_last_render = 0.0
        self.received_b64 = None
        self.dimensions = f"{meta['width']}x{meta['height']}"
        self.payload_size = meta["bytes"]
        self.status = f"Receiving from {sender}…"
        self._notify()

    def receive_row(self, row: bytes) -> None:
        """Append one scanline and (throttled) refresh the partial image."""
        pf = self._incoming
        if pf is None:
            return
        pf.add_row(row)
        now = time.monotonic()
        if pf.is_complete or now - self._incoming_last_render >= _RENDER_INTERVAL:
            self._incoming_last_render = now
            self.received_b64 = pf.render_b64()
            self.status = (
                f"Receiving from {self._incoming_sender}… "
                f"line {pf.rows_done}/{pf.rows_total}"
            )
            self._notify()

    def finish_receive(self, *, sender: str) -> None:
        """All rows arrived: promote the buffer to the current fax document."""
        pf = self._incoming
        if pf is None:
            return
        doc = pf.to_document()
        self._incoming = None
        self.current_fax = doc
        self.received_b64 = render_png_b64(doc)
        # Mirror onto the Scanned tab and adopt the sender's parameters so
        # the control bar / JSON export reflect the received document.
        self.scanned_preview_b64 = self.received_b64
        self.resolution = doc.width
        self.threshold = doc.threshold
        self.invert = doc.invert
        self.payload_size = doc.payload_size
        self.dimensions = f"{doc.width}x{doc.height}"
        self.status = f"Received {self.dimensions} from {sender} ({doc.payload_size} B)."
        self._notify()

    def abort_receive(self, reason: str) -> None:
        """Discard the receive buffer (a partial preview stays on screen)."""
        self._incoming = None
        self.status = reason
        self._notify()
