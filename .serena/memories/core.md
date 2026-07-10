# Core

## Project

Fax machine simulator — scan images into 1-bit packed bitmaps, transmit via JSON, render back as PNG. Two entry points: full app (`src/main.py`) and read-only viewer (`src/fax_reader.py`).

## Architecture: MVVM

```
src/
├── main.py                 # Full app entry (Scan + Read + Camera)
├── fax_reader.py           # Standalone read-only entry
├── models/                 # Data + logic
│   ├── fax_document.py     # FaxDocument dataclass + JSON ser/de
│   ├── scanner.py          # Image → 1-bit packed bitmap (BOX avg)
│   └── receiver.py         # Packed bitmap → base64 PNG
├── viewmodels/             # State + commands
│   ├── fax_viewmodel.py    # Full scan/read state, re-preview on param change
│   └── reader_viewmodel.py # Read-only state + load command
└── views/                  # UI components
    ├── components.py       # ImagePanel, StatusBar, ControlBar, spawn()
    ├── fax_view.py         # Side-by-side Scanned | Received layout
    └── reader_view.py      # Load + single image display
```

## Data flow

Control layer (main.py/fax_reader.py) handles async FilePicker/Camera → calls ViewModel methods → Model processes → ViewModel updates state + notifies → View callback rebuilds UI.

Re-preview: threshold slider / invert toggle re-runs scan on cached bytes (no disk re-read).

## Key design constraint

Never create per-pixel Flet controls. 1024×1024 fax = ~1M widgets. Instead, decode entire bitmap into one PIL Image and display via single `ft.Image` control.
