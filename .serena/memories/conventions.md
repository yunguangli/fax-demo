# Conventions

- **Architecture**: Strict MVVM. Models = pure logic. ViewModels = state + commands. Views = UI composition. Control layer (entry files) = async event handlers bridging Flet services (and lanlink network callbacks) to ViewModels.
- **lanlink boundary**: `src/lanlink/` is stdlib-only and extraction-ready — never import Flet or app modules (`models/`, `viewmodels/`, `views/`, entry files) into it. Fax-specific wire semantics (FAX1 magic, row size = width // 8) live in `src/network_protocol.py`, not in lanlink.
- **Wire vs storage**: JSON storage stays `version: 1`; the network envelope is separate (FAX1 handshake dict + raw row bytes). Do not conflate them.
- **Async**: All Flet entry handlers are `async def`. Camera/FilePicker calls are awaited. Async callbacks spawned from sync `on_click` via `spawn()` (returns/logs task refs; hang-up cancels them).
- **Type hints**: Used on function signatures. `from __future__ import annotations` in all files.
- **Docstrings**: Module-level docstrings describe purpose, architecture, and run commands. No per-method docstrings observed.
- **Naming**: snake_case for functions/variables, PascalCase for classes. Module names match concept (scanner, receiver, fax_document, line_viewmodel).
- **State updates**: ViewModel calls `_notify()` → view callback fires → reads VM state fields → updates controls → `page.update()`. `fax_view` subscribes BOTH `vm` and `line_vm` to one shared update function; progress notifications are throttled (~80 ms).
- **Image display**: Single `ft.Image(src=base64_png)` per fax — never per-pixel widgets.
- **Error handling**: try/except in control layer with `vm.set_status`/`line_vm.set_status` — no exceptions propagate to UI.
