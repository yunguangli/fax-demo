"""FaxDocument dataclass with JSON (de)serialization.

The bitmap payload is stored as base64 of the packed 1-bit bitmap in the
PIL mode "1" layout: 1 bit per pixel, MSB-first within each byte, row-major,
rows padded to byte boundary. For the supported square resolutions
(64/128/256/512/1024) the width is always a multiple of 8 so there is no
padding.

PIL mode "1" pixel semantics: 0 = black, 255 = white. The packed bit values
follow PIL's internal convention (bit 1 = white, bit 0 = black); this is an
internal detail that does not affect the scanner/receiver round-trip, since
Image.frombytes("1", ...) reproduces the same picture that tobytes() packed.
"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass, field

VERSION = 1


@dataclass
class FaxDocument:
    width: int
    height: int
    threshold: int
    data: bytes = field(repr=False)
    invert: bool = False

    @property
    def payload_size(self) -> int:
        """Size of the packed bitmap in bytes (not the base64 string length)."""
        return len(self.data)

    def to_json(self) -> str:
        return json.dumps(
            {
                "version": VERSION,
                "width": self.width,
                "height": self.height,
                "threshold": self.threshold,
                "invert": self.invert,
                "data": base64.b64encode(self.data).decode("ascii"),
            },
            ensure_ascii=True,
            indent=2,
        )

    @classmethod
    def from_json(cls, s: str) -> "FaxDocument":
        obj = json.loads(s)
        if obj.get("version") != VERSION:
            raise ValueError(
                f"Unsupported fax document version: {obj.get('version')!r} "
                f"(expected {VERSION})"
            )
        return cls(
            width=int(obj["width"]),
            height=int(obj["height"]),
            threshold=int(obj["threshold"]),
            invert=bool(obj.get("invert", False)),
            data=base64.b64decode(obj["data"]),
        )

    def __len__(self) -> int:
        return self.width * self.height
