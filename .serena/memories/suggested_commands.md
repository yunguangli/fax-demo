# Suggested Commands

## Run

- `uv run flet run` — desktop app
- `uv run flet run --web` — web app (use distinct `--port` per instance; one server = one fax identity)
- `uv run flet run src/fax_reader.py` — reader-only standalone

## Verify

- `uv run python -m py_compile src/<file>.py` — syntax check after edits (no test suite exists)
- Two-instance P2P test: start two `uv run flet run` consoles on this machine; each should list the other as a peer within ~3 s (beacon interval), ring ~1.8 s, then stream row-by-row (Normal ≈ 4 s/page; Turbo instant). Headsless harnesses from Phase 1 development: `/tmp/opencode/integration_fax.py`, `view_smoke.py`, `soak_discovery.py`.

## Build

- `flet build apk -v` — Android
- `flet build ipa -v` — iOS
- `flet build macos -v` — macOS
- `flet build linux -v` — Linux
- `flet build windows -v` — Windows
- `flet build web -v` — Web

## System (Linux)

- `ls`, `grep`, `find` — standard unix
