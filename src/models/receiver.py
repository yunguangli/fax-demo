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


class ProgressiveFax:
    """Row-by-row receive buffer for the network path.

    Rows arrive over the wire and are written straight into a packed
    mode-"1" bitmap; not-yet-received rows stay white (bit 1 = white, the
    same convention FaxDocument documents), so the partial image looks like
    paper feeding through a fax machine one scanline at a time.

    The buffer follows the same invariants as the scanner: width is a
    multiple of 8, rows are width // 8 bytes, row-major, no padding.
    """

    def __init__(
        self,
        width: int,
        height: int,
        *,
        threshold: int = 128,
        invert: bool = False,
    ) -> None:
        if width <= 0 or height <= 0 or width % 8 != 0:
            raise ValueError(f"invalid progressive dimensions: {width}x{height}")
        self.width = width
        self.height = height
        self.threshold = threshold
        self.invert = invert
        self._row_size = width // 8
        # All bits set => every pixel white until rows arrive.
        self._buf = bytearray(b"\xff" * (width * height // 8))
        self._rows_done = 0

    @property
    def row_size(self) -> int:
        return self._row_size

    @property
    def rows_done(self) -> int:
        return self._rows_done

    @property
    def rows_total(self) -> int:
        return self.height

    @property
    def is_complete(self) -> bool:
        return self._rows_done >= self.height

    def add_row(self, row: bytes) -> None:
        if self.is_complete:
            raise ValueError("all rows already received")
        if len(row) != self._row_size:
            raise ValueError(f"row has {len(row)} bytes, expected {self._row_size}")
        off = self._rows_done * self._row_size
        self._buf[off : off + self._row_size] = row
        self._rows_done += 1

    def to_document(self) -> FaxDocument:
        if not self.is_complete:
            raise ValueError(
                f"receive incomplete: {self._rows_done}/{self.height} rows"
            )
        return FaxDocument(
            self.width,
            self.height,
            self.threshold,
            bytes(self._buf),
            self.invert,
        )

    def render_b64(self) -> str:
        """Render current (possibly partial) contents to a base64 PNG."""
        img = Image.frombytes("1", (self.width, self.height), bytes(self._buf))
        return image_to_png_b64(img)
