"""Fax machine simulator — standalone reader entry point.

Read-only: load a fax JSON file and display the rendered black-and-white
image. No scan/save functionality. Uses the same Model + shared View
components as the full app.

Run:
    uv run python src/fax_reader.py
    uv run flet run src/fax_reader.py
"""

from __future__ import annotations

import flet as ft

from viewmodels import ReaderViewModel
from views import build_reader_view


async def main(page: ft.Page) -> None:
    page.title = "Fax Reader"
    page.padding = 20
    page.bgcolor = ft.Colors.GREY_900
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 520
    page.window.height = 640

    vm = ReaderViewModel()

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    async def on_load() -> None:
        files = await file_picker.pick_files(
            dialog_title="Pick a fax JSON file",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["json"],
            allow_multiple=False,
            with_data=True,
        )
        if not files:
            vm.set_status("Load cancelled.")
            return
        f = files[0]
        if f.bytes:
            try:
                vm.load_fax_from_text(f.bytes.decode("utf-8", errors="replace"))
            except Exception as ex:
                vm.set_status(f"Load failed: {ex}")
        elif f.path:
            try:
                with open(f.path, "r", encoding="utf-8") as fh:
                    vm.load_fax_from_text(fh.read())
            except OSError as ex:
                vm.set_status(f"Load failed: {ex}")
        else:
            vm.set_status("Load failed: no file data.")

    view = build_reader_view(page, vm, on_load=on_load)
    page.add(ft.SafeArea(content=view, expand=True))


if __name__ == "__main__":
    ft.run(main)
