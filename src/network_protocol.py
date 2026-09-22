"""FAX1 wire codec: maps FaxDocuments onto lanlink sessions.

The generic lanlink package knows nothing about faxes; this module defines
the fax-specific exchange that rides on top of it:

* handshake — JSON dict with the FAX1 magic + document metadata + the exact
  payload length, built by the sender and validated by the receiver before
  it rings.
* payload — the packed mode-"1" bitmap itself, row-major, unchanged from
  FaxDocument. Row size = width // 8 bytes (every supported resolution is a
  multiple of 8, so rows never need padding — the same invariant the
  scanner guarantees for version-1 JSON).

Wire flow (implemented by lanlink.session + main.py wiring):

    connect -> handshake {magic,sender,width,height,threshold,invert,bytes}
            -> BUSY or ring delay -> ok
            -> payload[bytes] streamed at line rate (or turbo)
            -> ok {bytes} -> close
"""

from __future__ import annotations

from lanlink.errors import HandshakeError

from models import FaxDocument

MAGIC = "FAX1"


def row_size(width: int) -> int:
    """Bytes per scanline in the packed bitmap (width is a multiple of 8)."""
    return width // 8


def build_handshake(doc: FaxDocument, *, sender: str) -> dict:
    """Create the FAX1 handshake for sending `doc`."""
    return {
        "magic": MAGIC,
        "sender": sender,
        "width": doc.width,
        "height": doc.height,
        "threshold": doc.threshold,
        "invert": doc.invert,
        "bytes": len(doc.data),
    }


def parse_handshake(header: dict) -> tuple[str, dict]:
    """Validate an incoming handshake.

    Returns `(sender, meta)` where meta holds width/height/threshold/invert/
    bytes. Raises HandshakeError on anything malformed or non-FAX1 so the
    session server can refuse the call before ringing.
    """
    if not isinstance(header, dict) or header.get("magic") != MAGIC:
        raise HandshakeError(f"not a FAX1 handshake: {header!r}")
    try:
        width = int(header["width"])
        height = int(header["height"])
        threshold = int(header["threshold"])
        nbytes = int(header["bytes"])
        invert = bool(header.get("invert", False))
        sender = str(header.get("sender") or "unknown peer")
    except (KeyError, TypeError, ValueError) as ex:
        raise HandshakeError(f"malformed FAX1 handshake: {ex}") from ex
    if width <= 0 or height <= 0 or width % 8 != 0:
        raise HandshakeError(f"invalid FAX1 dimensions: {width}x{height}")
    if nbytes != row_size(width) * height:
        raise HandshakeError(
            f"FAX1 payload length {nbytes} does not match {width}x{height}"
        )
    meta = {
        "width": width,
        "height": height,
        "threshold": threshold,
        "invert": invert,
        "bytes": nbytes,
    }
    return sender, meta


def split_rows(payload: bytes, width: int):
    """Yield individual scanlines from a packed bitmap payload."""
    size = row_size(width)
    for off in range(0, len(payload), size):
        yield payload[off : off + size]
