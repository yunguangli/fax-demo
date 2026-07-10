# Conventions

- **Architecture**: Strict MVVM. Models = pure logic. ViewModels = state + commands. Views = UI composition. Control layer (entry files) = async event handlers bridging Flet services to ViewModels.
- **Async**: All Flet entry handlers are `async def`. Camera/FilePicker calls are awaited.
- **Type hints**: Used on function signatures. `from __future__ import annotations` in all files.
- **Docstrings**: Module-level docstrings describe purpose, architecture, and run commands. No per-method docstrings observed.
- **Naming**: snake_case for functions/variables, PascalCase for classes. Module names match concept (scanner, receiver, fax_document).
- **State updates**: ViewModel calls `_notify()` → view callback fires → reads VM state fields → updates controls → `page.update()`.
- **Image display**: Single `ft.Image(src=base64_png)` per fax — never per-pixel widgets.
- **Error handling**: try/except in control layer with `vm.set_status(error_msg)` — no exceptions propagate to UI.
