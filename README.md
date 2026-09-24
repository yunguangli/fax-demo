# Fax app

A fax machine simulator built with [Flet](https://flet.dev/) (Python ≥ 3.10,
managed with [uv](https://docs.astral.sh/uv/), MVVM architecture). Scan any
image into a 1-bit black-and-white "fax page", then transmit it to another fax
on the network — the receiver prints it **line by line**, like paper feeding
through a real fax machine. Faxes can also be saved to and loaded from a
compact JSON file.

## Features

- **Scan** — load an image (or capture with the camera) and process it:
  center-crop to a square, resample to 64–1024², binarize with a live
  threshold slider and Invert switch, with Original / Grayscale / Scanned
  stage previews.
- **P2P line (LAN)** — instances announce themselves with UDP beacons and
  show up in each other's peer list automatically. Pick a peer, hit
  **Transmit**: the line rings twice, auto-answers, and streams the page at a
  simulated line rate (~4 s/page) — or instantly with the **Turbo** toggle.
  One line per machine: calling while a transfer is active answers **BUSY**,
  and **Hang up** aborts a call from either side.
- **Receive** — the incoming page fills progressively while it transfers;
  received faxes adopt the sender's parameters and can be saved as JSON.
- **Reader** — `src/fax_reader.py` is a separate read-only viewer that just
  loads and displays fax JSON files.

## JSON format

Faxes are stored as `version: 1` JSON:

```json
{"version": 1, "width": 512, "height": 512, "threshold": 128,
 "invert": false, "data": "<base64 of the packed mode-1 bitmap>"}
```

The network wire format is separate (an `FAX1` handshake + raw row bytes) and
does not change this storage format.

## Project layout

```
src/
├── main.py              # full app entry (Scan + Receive + Camera + line)
├── fax_reader.py        # read-only viewer entry
├── network_protocol.py  # FAX1 codec (fax semantics over lanlink)
├── lanlink/             # reusable stdlib-only P2P package
│                        #   (multicast discovery + ringed/paced TCP sessions)
├── models/              # FaxDocument JSON, scanner, renderer, ProgressiveFax
├── viewmodels/          # state + commands (MVVM)
└── views/               # Flet UI (line panel, panels, control bar)
```

## Try the P2P line

Open **two** instances — one process is one fax identity, so two terminals:

```bash
uv run flet run   # terminal 1
uv run flet run   # terminal 2
```

Each lists the other as a peer within ~3 s. Scan an image in one, select the
peer, press **Transmit**, and watch the other's *Receive* tab fill line by
line.

> **Cross-machine play (firewall):** two instances on *one* machine never
> touch your firewall (loopback is always allowed), but a second device does
> — each desktop must admit inbound **UDP 47555** (peer beacons) and
> **TCP 47554** (the call). With ufw:
>
> ```bash
> sudo ufw allow from 192.168.1.0/24 to any port 47555 proto udp comment 'lanlink discovery'
> sudo ufw allow from 192.168.1.0/24 to any port 47554 proto tcp comment 'lanlink calls'
> ```
>
> Use your own subnet (check with `ip -br addr`). Without the rules the
> symptom is **one-way discovery**: the other fax sees you, but you never
> see it.

## Run the app

### uv

Run as a desktop app:

```bash
uv run flet run
```

Run as a web app:

```bash
uv run flet run --web
```

Run the read-only fax reader:

```bash
uv run flet run src/fax_reader.py
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/).

## Build the app

### Android

```bash
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```bash
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```bash
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```bash
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```bash
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).

### Web

```bash
flet build web -v
```

For more details on building Web app, refer to the [Web Packaging Guide](https://flet.dev/docs/publish/web/).
