"""ReaderViewModel: read-only subset for the standalone fax_reader entry point.

Holds just enough state to load a JSON fax document and render its image.
The View subscribes via `on_changed` and re-reads state after every command.
"""

from __future__ import annotations

from typing import Callable, Optional

from models import FaxDocument, render_png_b64


class ReaderViewModel:
    def __init__(self) -> None:
        self.current_fax: Optional[FaxDocument] = None
        self.received_b64: Optional[str] = None
        self.status: str = "No fax loaded."
        self.payload_size: int = 0
        self.dimensions: str = ""
        # View subscribes here.
        self.on_changed: Optional[Callable[[], None]] = None

    def _notify(self) -> None:
        if self.on_changed is not None:
            self.on_changed()

    def set_status(self, text: str) -> None:
        """Allow the Control layer to report FilePicker outcomes."""
        self.status = text
        self._notify()

    def load_fax_from_text(self, json_text: str) -> None:
        try:
            doc = FaxDocument.from_json(json_text)
        except Exception as ex:
            self.current_fax = None
            self.received_b64 = None
            self.payload_size = 0
            self.dimensions = ""
            self.status = f"Load failed: {ex}"
            self._notify()
            return
        self.current_fax = doc
        self.received_b64 = render_png_b64(doc)
        self.payload_size = doc.payload_size
        self.dimensions = f"{doc.width}x{doc.height}"
        self.status = "Fax loaded."
        self._notify()

    def clear(self) -> None:
        self.current_fax = None
        self.received_b64 = None
        self.payload_size = 0
        self.dimensions = ""
        self.status = "Cleared."
        self._notify()
