"""Fax machine simulator — ViewModel layer.

ViewModels hold observable state and command methods. They expose a single
`on_changed` callback slot that the View subscribes to; every state mutation
calls `_notify()`, which invokes the callback. The View is responsible for
re-reading VM state and updating its Flet controls + calling page.update().

ViewModels have no Flet dependency. They accept async callbacks (for file
picker / camera results) so the Control layer (in main.py / fax_reader.py)
can pass through file paths or raw bytes returned by those services.
"""

from .fax_viewmodel import FaxViewModel
from .reader_viewmodel import ReaderViewModel

__all__ = ["FaxViewModel", "ReaderViewModel"]
