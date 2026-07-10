"""Reader-only view: load a JSON fax and display the received image.

Used by the standalone `fax_reader.py` entry point. Reuses ImagePanel and
StatusBar from components.py so the look matches the full fax app.
"""

from __future__ import annotations

from typing import Awaitable, Callable

import flet as ft

from .components import ImagePanel, StatusBar, spawn


def build_reader_view(
    page: ft.Page,
    vm,
    *,
    on_load: Callable[[], Awaitable[None]],
) -> ft.Control:
    """Build the read-only fax UI and bind it to the ReaderViewModel."""

    received_panel = ImagePanel("Received fax", height=420)
    status_bar = StatusBar()

    load_btn = ft.FilledButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.FOLDER_OPEN, size=18), ft.Text(value="Load fax JSON")],
            spacing=8,
        ),
        on_click=lambda e: spawn(on_load),
    )

    clear_btn = ft.Button(
        content=ft.Text(value="Clear"),
        on_click=lambda e: vm.clear(),
    )

    button_row = ft.Row(
        controls=[load_btn, clear_btn],
        spacing=10,
    )

    root = ft.Column(
        controls=[button_row, received_panel, status_bar],
        spacing=10,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def update_view() -> None:
        received_panel.set_image(vm.received_b64)
        status_bar.update_state(vm.dimensions, vm.payload_size, vm.status)
        page.update()

    vm.on_changed = update_view
    update_view()
    return root

