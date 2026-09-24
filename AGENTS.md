# AGENTS.md

## Project

- Fax machine simulator (Flet desktop/web app, Python `>=3.10`, uv, strict MVVM): scan images into 1-bit fax pages, transmit them P2P over the LAN to another running instance (peer discovery + a single ringed, paced phone line), render received pages line by line while they transfer, and save/load faxes as `version: 1` JSON.
- Two entry points: `src/main.py` (full app: Scan + Receive + Camera + P2P line) and `src/fax_reader.py` (read-only viewer, no networking). The reusable transport lives in `src/lanlink/`; fax-specific wire semantics in `src/network_protocol.py`.
- Human-facing description, feature list, and usage live in `README.md`; the sections below are the agent-facing rules and gotchas.

## Project and commands

- Small single-package Flet desktop/web app (not a monorepo). Python `>=3.10` managed with `uv`; `[tool.flet.app] path = "src"` in `pyproject.toml` selects the app entry point.
- Full desktop app: `uv run flet run`
- Full web app: `uv run flet run --web`
- Read-only viewer: `uv run flet run src/fax_reader.py` (or `uv run python src/fax_reader.py`)
- Package builds use the documented form `flet build <target> -v`, where `<target>` is `apk`, `ipa`, `macos`, `linux`, `windows`, or `web`.
- No test, lint, formatter, typecheck, codegen, or CI configuration is present (`.github/` contains only the Flet skill, no workflows). After edits, use `uv run python -m py_compile src/<file>.py` for syntax verification; do not invent a test command.
- Manual P2P verification: run **two** `uv run flet run` consoles on the same machine (one process = one fax identity, default name `Fax-<pid>`); two tabs against one server are the same instance, not a peer pair. Headless checks live outside the repo in `/tmp/opencode/` and are **ephemeral** (wiped on reboot — recreate rather than expecting old names); the current set is `regression_fax.py` (discovery + fixed port + payload + BUSY + hang-up,8 checks) and `port_fallback_smoke.py`.
- Cross-machine LAN needs inbound firewall holes on the desktop side: **UDP `47555`** (beacons) + **TCP `47554`** (calls). ufw's default deny drops inbound silently while same-host tests keep passing (loopback is always allowed) — the classic symptom is one-way discovery (they see you, you don't see them). `SessionServer.start()` binds the fixed `DEFAULT_TCP_PORT = 47554` (exported from `lanlink`) so the rule has a stable target, falling back to an ephemeral port when a second instance already holds it; the beacon advertises whichever port was bound. Documented for users in README's "Try the P2P line" section.
- Gotcha: `.gitignore` ignores `*.lock`, so `uv.lock` is untracked — `uv add`/`uv lock` changes will not appear in `git status`. Force-add it (`git add -f uv.lock`) if dependency changes should be committed.

## Imports

- Cross-layer imports are absolute from the `src/` root (`from models import ...`, `from viewmodels import ...`, `from views import ...`, `from lanlink import ...`, `from network_protocol import ...`); intra-package imports are relative (`from .components import ...`, `from .discovery import ...`). This only works because Flet (and running `python src/<entry>.py`, whose script dir becomes `sys.path[0]`) puts `src/` on `sys.path` — do not add a `src.` package prefix or restructure into an installable package.

## Architecture and behavior

- `src/main.py` is the full Scan + Receive + Camera + P2P line entry point. `src/fax_reader.py` is a separate read-only entry point (no networking).
- `src/lanlink/` is a **reusable, stdlib-only P2P package** (UDP multicast/broadcast discovery + ringed, paced TCP sessions) intended to be extracted into its own repo once the protocol stabilizes. Boundary rule: it must never import Flet or any app module (`models/`, `viewmodels/`, `views/`, entry files) — keep it extraction-ready. Fax-specific semantics live in `src/network_protocol.py` (FAX1 handshake dict, row size = width // 8) and `models/receiver.py` (`ProgressiveFax`).
- Line behavior (Phase 1, LAN only; `Peer.host` + `dial(host, port)` + versioned beacon/handshake are the Phase-2 internet seams): single line per machine (any non-IDLE state answers BUSY), auto-answer after 2 simulated rings (~1.8 s), Normal pacing targets ~4 s/page while Turbo sends at full speed. The receiver feeds rows into `ProgressiveFax` **as chunks arrive** (`conn.iter_payload` streaming — never read-then-render at the end) and re-renders the partial image at ~40 ms cadence so the page fills line by line; line-panel progress counters notify at ~80 ms. Discovery beacons go to multicast `239.255.42.99:47555` (default-if + loopback) plus a limited-broadcast fallback; plain broadcast alone does not fan out to same-host instances on Linux.
- Storage JSON stays `version: 1`; the wire format is separate (FAX1 handshake + raw row bytes, row size = width/8) and must not be conflated with the JSON envelope.
- Keep the MVVM boundaries: `models/` owns data and image/serialization logic; `viewmodels/` owns state and commands (including `LineViewModel`); `views/` composes Flet controls; entry files handle async Flet services and bridge results — `main.py` also bridges lanlink callbacks (discovery → `line_vm.set_peers`, sessions → begin/receive/finish/abort commands).
- Viewmodels notify through `on_changed`; views read state, update controls, and call `page.update()`. Source selection only caches/previews the image—an explicit Scan command runs the pipeline. Parameter changes re-scan cached source bytes only after a scan exists.
- Scanner behavior is non-negotiable for JSON compatibility: center-crop to a square, BOX-resample to 64/128/256/512/1024, binarize at threshold 0–255 (darker is black unless Invert), then store a base64-packed PIL mode-`1` bitmap in version-1 JSON (`version` field must stay `1`).
- Render the whole fax through one `ft.Image(src=base64_png)` control. Never create one Flet control per pixel; a 1024x1024 fax would otherwise create about one million widgets.
- Flet handlers are async when they await FilePicker/Camera APIs. The shared `spawn()` helper in `views/components.py` launches async callbacks from synchronous `on_click` handlers. Register the FilePicker with `page.services` (`main.py`) or `page.overlay` (`fax_reader.py`) as the entry point does.
- The camera must be mounted in the visual tree to work on web and may be unavailable on some platforms. Reference: https://flet.dev/docs/services/filepicker.
- FilePicker gotchas (Flet 1.0): `save_file` requires `src_bytes` on web/mobile and writes those bytes to the chosen file itself on desktop (`main.py:on_save` relies on this — no app-side write). `FilePickerFile.path` is always `None` on web, so pass `with_data=True` and fall back to `f.bytes` (both entry points do). A transient `ft.FilePicker()` constructed *inside* an event handler auto-registers via `Service.init()` using the ambient page context; constructed outside any callback it stays unregistered and method calls raise `RuntimeError` — prefer the shared registered picker. Awaited `pick_files()` from `on_click` silently fails in iOS Safari (browser gesture requirement); full web support needs `action=ft.PickFiles(...)` + `on_result`.
- For Flet API work, consult `.github/skills/flet-development/SKILL.md` (covers Flet >=0.82 breaking changes; largely in Chinese) and verify uncertain APIs against the installed Flet version with `inspect`; do not guess from older Flet examples.
- Serena MCP keeps notes in `.serena/memories/`; keep them in sync if conventions or commands change.
