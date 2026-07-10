"""Receiver: render a FaxDocument to a base64 PNG for display in ft.Image."""

from __future__ import annotations

import base64
from io import BytesIO

from PIL import Image

from .fax_document import FaxDocument


def render_png_b64(doc: FaxDocument) -> str:
    """Render the packed 1-bit bitmap to a base64-encoded PNG for ft.Image.

    Image.frombytes("1", (w, h), data) reconstructs the exact picture that
    the scanner packed via Image.tobytes(), then we encode it as PNG and
    base64-encode the PNG bytes so it can be passed directly to ft.Image(src=...).
    """
    if doc.width <= 0 or doc.height <= 0:
        raise ValueError(f"invalid dimensions: {doc.width}x{doc.height}")
    expected = (doc.width + 7) // 8 * doc.height
    if len(doc.data) < expected:
        raise ValueError(
            f"data too short: {len(doc.data)} bytes, expected at least {expected}"
        )
    img = Image.frombytes("1", (doc.width, doc.height), doc.data)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


def image_to_png_b64(image: "Image.Image") -> str:
    """Render any PIL image (RGB / L / 1) to a base64-encoded PNG for ft.Image."""
    buf = BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")
