# Core

## Project

Fax machine simulator — scan images into 1-bit packed bitmaps, transmit them P2P over the LAN like a real fax machine, render back as PNG line-by-line. Two entry points: full app (`src/main.py`) + read-only viewer (`src/fax_reader.py`, no networking).

## Architecture: MVVM

```
src/
├── main.py                 # Full app entry (Scan + Read + Camera + P2P line wiring)
├── fax_reader.py           # Standalone read-only entry
├── network_protocol.py     # FAX1 codec: FaxDocument <-> lanlink handshake/rows
├── lanlink/                # REUSABLE stdlib-only P2P package (extraction-ready)
│   ├── discovery.py        #   multicast/broadcast beacons + expiring peer table
│   ├── session.py          #   Connection, SessionServer (ring/BUSY), dial (paced)
│   └── errors.py           #   LineBusy, PeerGone, HandshakeError, TransferAborted
├── models/                 # Data + logic
│   ├── fax_document.py     # FaxDocument dataclass + JSON ser/de (version:1)
│   ├── scanner.py          # Image → 1-bit packed bitmap (BOX avg)
│   └── receiver.py         # Packed bitmap → base64 PNG + ProgressiveFax
├── viewmodels/             # State + commands
│   ├── fax_viewmodel.py    # Scan/read + begin/receive/finish/abort_receive
│   ├── line_viewmodel.py   # Peers, line states (IDLE/DIALING/RINGING/SENDING/RECEIVING), progress, turbo
│   └── reader_viewmodel.py # Read-only state + load command
└── views/                  # UI components
    ├── components.py       # ImagePanel, StatusBar, ControlBar, spawn()
    ├── fax_view.py         # Line panel + side-by-side Scanned | Received
    ├── line_panel.py       # Peer picker, Transmit/Hang up, turbo, line status
    └── reader_view.py      # Load + single image display
```

## Data flow

Control layer (main.py/fax_reader.py) handles async FilePicker/Camera → calls ViewModel methods → Model processes → ViewModel updates state + notifies → View callback rebuilds UI.

Re-preview: threshold slider / invert toggle re-runs scan on cached bytes (no disk re-read).

## P2P line (Phase 1, LAN)

Discovery beacons (multicast 239.255.42.99:47555 + limited-broadcast fallback; plain broadcast does NOT fan out to same-host instances on Linux — loopback multicast is the proven same-host path) feed `line_vm.set_peers`. Call flow: dial → FAX1 handshake → BUSY if receiver non-IDLE, else 2-ring delay (~1.8 s) → ACK → payload paced to ~4 s/page in 20 ms quanta (Turbo = full speed) → OK+byte count. Receiver streams rows into `ProgressiveFax` AS CHUNKS ARRIVE (`conn.iter_payload` — never read-all-then-render; that bug made the page pop in at the end) and re-renders the partial image at ~40 ms cadence for a live line-by-line fill. `main.py` owns the bridge (on_transmit/on_hangup/_on_incoming); `spawn()` task refs allow hang-up cancellation.

## Key design constraint

Never create per-pixel Flet controls. 1024×1024 fax = ~1M widgets. Instead, decode entire bitmap into one PIL Image and display via single `ft.Image` control.
