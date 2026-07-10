# Tech Stack

- **Language**: Python ≥3.10
- **UI framework**: Flet (>=0.85.3) — cross-platform Flutter-based Python UI
- **Additional deps**: `flet-camera`, `Pillow`
- **Dev deps**: `flet-cli`, `flet-desktop`, `flet-web` (all >=0.85.3)
- **Build/dep manager**: `uv` (lockfile: `uv.lock`)
- **Flet config**: `pyproject.toml → [tool.flet]` (org=com.mycompany, product=fax)
- **Image processing**: Pillow (PIL) — grayscale conversion, BOX resampling, 1-bit mode
- **Serialization**: JSON with base64-encoded packed bitmaps
