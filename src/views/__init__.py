"""Fax machine simulator — View layer (pure Flet UI, no business logic)."""

from .components import ImagePanel, StatusBar, PLACEHOLDER_PNG_B64
from .fax_view import build_fax_view
from .line_panel import LinePanel
from .reader_view import build_reader_view

__all__ = [
    "ImagePanel",
    "StatusBar",
    "PLACEHOLDER_PNG_B64",
    "build_fax_view",
    "build_reader_view",
    "LinePanel",
]
