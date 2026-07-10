"""Fax machine simulator — Model layer (no Flet dependency)."""

from .fax_document import FaxDocument
from .scanner import (
    scan,
    scan_from_bytes,
    scan_stages,
    scan_stages_from_bytes,
    ScanStages,
    original_png_b64,
    DEFAULT_RESOLUTION,
    DEFAULT_THRESHOLD,
    DEFAULT_INVERT,
)
from .receiver import render_png_b64, image_to_png_b64

__all__ = [
    "FaxDocument",
    "scan",
    "scan_from_bytes",
    "scan_stages",
    "scan_stages_from_bytes",
    "ScanStages",
    "original_png_b64",
    "render_png_b64",
    "image_to_png_b64",
    "DEFAULT_RESOLUTION",
    "DEFAULT_THRESHOLD",
    "DEFAULT_INVERT",
]
