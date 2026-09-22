"""Full fax view: scan + read side-by-side, with control bar.

`build_fax_view` composes the shared components, wires parameter-change
events directly to the ViewModel (sync), and wires action buttons to async
callbacks provided by the Control layer. It subscribes the view's update
function to `vm.on_changed`.
"""

from __future__ import annotations

from typing import Awaitable, Callable

import flet as ft

from .components import ImagePanel, ScanStagePanel, StatusBar, make_control_bar, spawn
from .line_panel import LinePanel


async def _async_noop() -> None:
    """Awaitable placeholder for optional line callbacks (e.g. reader view)."""


def build_fax_view(
    page: ft.Page,
    vm,
    *,
    on_scan: Callable[[], Awaitable[None]],
    on_scan_run: Callable[[], Awaitable[None]],
    on_save: Callable[[], Awaitable[None]],
    on_load: Callable[[], Awaitable[None]],
    extra_buttons: list | None = None,
    line_vm=None,
    on_transmit: Callable[[], Awaitable[None]] | None = None,
    on_hangup: Callable[[], Awaitable[None]] | None = None,
) -> ft.Control:
    """Build the full fax UI and bind it to the ViewModel.

    Returns the root control. The caller (Control layer) is expected to
    `page.add()` it after registering any service controls (FilePicker, etc).

    `on_scan` loads/picks a source image (shows it in tab 1 but does not
    process it); `on_scan_run` runs the actual scan pipeline.

    `line_vm` (optional) adds the P2P line panel to the Scan tab; the view
    then subscribes to *both* ViewModels with the same update function.
    """

    scanned_panel = ScanStagePanel()
    received_panel = ImagePanel("Received")
    status_bar = StatusBar()
    receive_status_bar = StatusBar()

    # Tab 1 (Scan) buttons, two rows:
    #   Row 1 (source): ft.Row([Load Image, Camera])
    #   Row 2 (action): ft.Row([Scan, Save])
    load_image_btn = ft.Button(
        content=ft.Row(
            [ft.Icon(ft.Icons.FOLDER_OPEN, size=18), ft.Text(value="Load Image")],
            spacing=8,
        ),
        on_click=lambda e: spawn(on_scan),
    )
    source_row = ft.Row(
        controls=[load_image_btn, *(extra_buttons or [])],  # Load Image first, then Camera
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    scan_btn = ft.FilledButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.DOCUMENT_SCANNER, size=18), ft.Text(value="Scan")],
            spacing=8,
        ),
        on_click=lambda e: spawn(on_scan_run),
    )
    save_btn = ft.Button(
        content=ft.Row(
            [ft.Icon(ft.Icons.SAVE, size=18), ft.Text(value="Save")],
            spacing=8,
        ),
        on_click=lambda e: spawn(on_save),
    )
    clear_scan_btn = ft.Button(
        content=ft.Row(
            [ft.Icon(ft.Icons.CLEAR, size=18), ft.Text(value="Clear")],
            spacing=8,
        ),
        on_click=lambda e: (vm.clear(), page.update()),
    )
    action_row = ft.Row(
        controls=[scan_btn, save_btn, clear_scan_btn],
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    control_bar, refresh_control_bar = make_control_bar(
        resolution=vm.resolution,
        on_resolution=vm.set_resolution,
        threshold=vm.threshold,
        on_threshold=vm.set_threshold,
        invert=vm.invert,
        on_invert=vm.set_invert,
        source_row=source_row,
        action_row=action_row,
    )

    # P2P line panel (only wired in main.py; fax_reader passes no line_vm).
    line_panel: LinePanel | None = None
    if line_vm is not None:
        line_panel = LinePanel(
            line_vm,
            on_transmit=on_transmit or _async_noop,
            on_hangup=on_hangup or _async_noop,
        )

    scan_tab = ft.Column(
        controls=[control_bar, *([line_panel] if line_panel else []), scanned_panel, status_bar],
        spacing=10,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    # Tab 2 (Receive): Load JSON + Received image.
    load_btn = ft.FilledButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.FOLDER_OPEN, size=18), ft.Text(value="Load JSON")],
            spacing=8,
        ),
        on_click=lambda e: spawn(on_load),
    )
    clear_btn = ft.Button(
        content=ft.Text(value="Clear"),
        on_click=lambda e: (vm.clear(), page.update()),
    )
    receive_tab = ft.Column(
        controls=[
            ft.Row(controls=[load_btn, clear_btn], spacing=10, wrap=True),
            received_panel,
            receive_status_bar,
        ],
        spacing=10,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    root = ft.Tabs(
        length=2,
        selected_index=0,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="Scan", icon=ft.Icons.CAMERA_ALT),
                        ft.Tab(label="Receive", icon=ft.Icons.FOLDER_OPEN),
                    ],
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[scan_tab, receive_tab],
                ),
            ],
        ),
    )

    def update_view() -> None:
        # Keep the control bar widgets in sync with the ViewModel: loading a
        # fax adopts its resolution/threshold/invert, and stale widget values
        # would otherwise clobber the loaded parameters on the next change.
        refresh_control_bar(vm.resolution, vm.threshold, vm.invert)
        scanned_panel.set_images(
            vm.original_b64, vm.grayscale_b64, vm.scanned_preview_b64
        )
        received_panel.set_image(vm.received_b64)
        status_bar.update_state(vm.dimensions, vm.payload_size, vm.status)
        receive_status_bar.update_state(vm.dimensions, vm.payload_size, vm.status)
        if line_panel is not None:
            line_panel.refresh(can_transmit=vm.current_fax is not None)
        page.update()

    vm.on_changed = update_view
    if line_vm is not None:
        # Both ViewModels share one subscriber, so a peer/line notification
        # refreshes the whole view (and vice versa) with a single update.
        line_vm.on_changed = update_view
    update_view()
    return root
