"""Scanner: rasterize an image into a 1-bit fax document.

Pipeline:
1. Open image, convert to grayscale ("L").
2. Resize to (resolution, resolution) with BOX resampling — BOX computes the
   exact average of source pixels in each output cell, which is exactly the
   "average grayscale per cell" step in the spec.
3. Binarize with a threshold; conventionally darker-than-threshold -> black
   (PIL "1" bit = 1), brighter -> white (0). Invert flips the comparison.
4. Pack the 1-bit pixels via PIL mode "1" tobytes() and store on FaxDocument.

The source can come from a file path (FilePicker result) or raw bytes
(Camera.take_picture() result), so both entry points are provided.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

from PIL import Image

from .fax_document import FaxDocument

DEFAULT_RESOLUTION = 256
DEFAULT_THRESHOLD = 128
DEFAULT_INVERT = False

VALID_RESOLUTIONS = (64, 128, 256, 512, 1024)


def _binarize(gray_img: Image.Image, threshold: int, invert: bool) -> Image.Image:
    """Return a PIL mode '1' image.

    PIL mode '1' pixel values: 0 = black, 255 = white.
    Default convention: darker-than-threshold -> black (0).
    Invert flips the comparison so bright pixels become black instead.
    """
    if invert:
        # bright -> black
        def mapping(p: int) -> int:
            return 0 if p >= threshold else 255
    else:
        # dark -> black
        def mapping(p: int) -> int:
            return 0 if p < threshold else 255

    return gray_img.point(mapping, mode="1")


@dataclass
class ScanStages:
    """Intermediate images plus the final fax document produced by one scan."""

    original: "Image.Image"
    grayscale: "Image.Image"
    document: FaxDocument


def _run_pipeline(
    img: Image.Image,
    resolution: int = DEFAULT_RESOLUTION,
    threshold: int = DEFAULT_THRESHOLD,
    invert: bool = DEFAULT_INVERT,
) -> ScanStages:
    if resolution not in VALID_RESOLUTIONS:
        raise ValueError(
            f"resolution must be one of {VALID_RESOLUTIONS}, got {resolution}"
        )
    if not 0 <= threshold <= 255:
        raise ValueError(f"threshold must be 0..255, got {threshold}")

    original = img.convert("RGB")
    gray = original.convert("L")
    # Crop to square so the cell grid is uniform (cells must be square to
    # match the WxH resolution exactly with no remainder).
    w, h = gray.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    gray = gray.crop((left, top, left + side, top + side))
    # Average-grayscale per cell: BOX filter is exactly box-average.
    gray = gray.resize((resolution, resolution), Image.Resampling.BOX)

    bw = _binarize(gray, threshold, invert)
    document = FaxDocument(
        width=resolution,
        height=resolution,
        threshold=threshold,
        invert=invert,
        data=bw.tobytes(),
    )
    return ScanStages(original=original, grayscale=gray, document=document)


def _scan_pil(
    img: Image.Image,
    resolution: int = DEFAULT_RESOLUTION,
    threshold: int = DEFAULT_THRESHOLD,
    invert: bool = DEFAULT_INVERT,
) -> FaxDocument:
    return _run_pipeline(img, resolution, threshold, invert).document


def scan(
    image_path: str,
    resolution: int = DEFAULT_RESOLUTION,
    threshold: int = DEFAULT_THRESHOLD,
    invert: bool = DEFAULT_INVERT,
) -> FaxDocument:
    """Scan an image file into a FaxDocument."""
    with Image.open(image_path) as img:
        # Load into memory so the file handle can close before processing.
        img.load()
        return _scan_pil(img, resolution, threshold, invert)


def scan_from_bytes(
    image_bytes: bytes,
    resolution: int = DEFAULT_RESOLUTION,
    threshold: int = DEFAULT_THRESHOLD,
    invert: bool = DEFAULT_INVERT,
) -> FaxDocument:
    """Scan an in-memory image (e.g. from Camera.take_picture()) into a FaxDocument."""
    with Image.open(BytesIO(image_bytes)) as img:
        img.load()
        return _scan_pil(img, resolution, threshold, invert)


def scan_stages(
    image_path: str,
    resolution: int = DEFAULT_RESOLUTION,
    threshold: int = DEFAULT_THRESHOLD,
    invert: bool = DEFAULT_INVERT,
) -> ScanStages:
    """Scan an image file, returning the original, grayscale and fax stages."""
    with Image.open(image_path) as img:
        img.load()
        return _run_pipeline(img, resolution, threshold, invert)


def scan_stages_from_bytes(
    image_bytes: bytes,
    resolution: int = DEFAULT_RESOLUTION,
    threshold: int = DEFAULT_THRESHOLD,
    invert: bool = DEFAULT_INVERT,
) -> ScanStages:
    """Scan in-memory image bytes, returning the original, grayscale and fax stages."""
    with Image.open(BytesIO(image_bytes)) as img:
        img.load()
        return _run_pipeline(img, resolution, threshold, invert)


def original_png_b64(image_bytes: bytes) -> str:
    """Render the (un-cropped, RGB) source image to a base64 PNG for preview."""
    from .receiver import image_to_png_b64

    with Image.open(BytesIO(image_bytes)) as img:
        img.load()
        return image_to_png_b64(img.convert("RGB"))
