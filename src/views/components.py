"""Shared Flet UI components for the fax simulator.

These are pure view helpers — they know nothing about ViewModels or the
Control layer. The fax_view and reader_view modules compose them and wire
them to ViewModel state.
"""

from __future__ import annotations

import asyncio
from typing import Awaitable, Callable

import flet as ft


def spawn(coro_func: Callable[[], Awaitable[None]]) -> None:
    """Fire-and-forget an async callable from a sync on_click handler."""
    asyncio.create_task(coro_func())

# A 1x1 transparent PNG used as the initial image placeholder so ft.Image
# always has a valid src (avoids rendering errors before any scan/load).
PLACEHOLDER_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wIAAgMBAp0YVwAAAABJRU5ErkJggg=="
)


class ImagePanel(ft.Container):
    """A titled panel that displays a base64-PNG image with a checkerboard-free
    black background so black fax pixels are visible against the panel.

    Call `set_image(src_b64_or_bytes)` to update the displayed image.
    """

    def __init__(self, title: str, *, height: int = 320) -> None:
        self._title_text = ft.Text(
            value=title,
            size=14,
            weight=ft.FontWeight.BOLD,
        )
        self._image = ft.Image(
            src=PLACEHOLDER_PNG_B64,
            fit=ft.BoxFit.CONTAIN,
            gapless_playback=True,
        )
        self._empty_hint = ft.Text(
            value="No image yet",
            size=12,
            color=ft.Colors.GREY_500,
            visible=False,
        )
        super().__init__(
            expand=True,
            bgcolor=ft.Colors.BLACK,
            border_radius=ft.BorderRadius.all(6),
            padding=ft.Padding.all(8),
            content=ft.Column(
                expand=True,
                controls=[
                    self._title_text,
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Stack(
                            expand=True,
                            controls=[self._image, self._empty_hint],
                        ),
                    ),
                ],
            ),
            height=height,
        )

    def set_image(self, src) -> None:
        """Update the image source. Pass a base64 string, raw bytes, or None."""
        if src is None:
            self._image.visible = False
            self._empty_hint.visible = True
        else:
            self._image.visible = True
            self._image.src = src
            self._empty_hint.visible = False


class ScanStagePanel(ft.Container):
    """Scanned-preview panel shown as three tabs:

    - Original   : the source image as captured/loaded (tab 1)
    - Grayscale  : the square, BOX-averaged grayscale fed to the binarizer (tab 2)
    - Scanned    : the binarized fax output (tab 3)

    Call `set_images(original, grayscale, scanned)` with base64-PNG strings
    (or None for a stage that is not available yet).
    """

    def __init__(self, *, height: int = 320) -> None:
        self._original = self._make_image()
        self._grayscale = self._make_image()
        self._scanned = self._make_image()

        tabs = ft.Tabs(
            length=3,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Original"),
                            ft.Tab(label="Grayscale"),
                            ft.Tab(label="Scanned"),
                        ],
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=self._original,
                                expand=True,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=self._grayscale,
                                expand=True,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=self._scanned,
                                expand=True,
                                alignment=ft.Alignment.CENTER,
                            ),
                        ],
                    ),
                ],
            ),
        )

        super().__init__(
            expand=True,
            bgcolor=ft.Colors.BLACK,
            border_radius=ft.BorderRadius.all(6),
            padding=ft.Padding.all(8),
            content=ft.Column(
                expand=True,
                controls=[tabs],
            ),
            height=height,
        )

    @staticmethod
    def _make_image() -> ft.Image:
        return ft.Image(
            src=PLACEHOLDER_PNG_B64,
            fit=ft.BoxFit.CONTAIN,
            gapless_playback=True,
        )

    def set_images(self, original, grayscale, scanned) -> None:
        """Update the three stage images. Pass None for any unavailable stage."""
        self._original.visible = original is not None
        self._grayscale.visible = grayscale is not None
        self._scanned.visible = scanned is not None
        if original is not None:
            self._original.src = original
        if grayscale is not None:
            self._grayscale.src = grayscale
        if scanned is not None:
            self._scanned.src = scanned


class StatusBar(ft.Container):
    """A one-line status bar showing dimensions, payload size, and message."""

    def __init__(self) -> None:
        self._dims = ft.Text(value="\u2014", size=12, color=ft.Colors.GREY_400)
        self._payload = ft.Text(value="\u2014", size=12, color=ft.Colors.GREY_400)
        self._status = ft.Text(
            value="Ready.",
            size=12,
            color=ft.Colors.GREY_300,
            expand=True,
        )
        super().__init__(
            bgcolor=ft.Colors.GREY_900,
            border_radius=ft.BorderRadius.all(4),
            padding=ft.Padding.symmetric(horizontal=10, vertical=6),
            content=ft.Row(
                controls=[
                    ft.Text(value="dims:", size=11, color=ft.Colors.GREY_500),
                    self._dims,
                    ft.Text(value="payload:", size=11, color=ft.Colors.GREY_500),
                    self._payload,
                    self._status,
                ],
                spacing=8,
            ),
        )

    def update_state(self, dimensions: str, payload_size: int, status: str) -> None:
        self._dims.value = dimensions or "\u2014"
        if payload_size > 0:
            self._payload.value = f"{payload_size} B"
        else:
            self._payload.value = "\u2014"
        self._status.value = status


def make_control_bar(
    *,
    resolution: int,
    on_resolution,
    threshold: int,
    on_threshold,
    invert: bool,
    on_invert,
    source_row,
    action_row,
):
    """Build the top control bar (resolution/threshold/invert + two button rows).

    `source_row` and `action_row` are `ft.Row` controls already containing the
    buttons (e.g. `ft.Row(controls=[load_btn, camera_btn])`).
    """
    resolution_dd = ft.Dropdown(
        value=str(resolution),
        width=140,
        label="Resolution",
        options=[
            ft.DropdownOption(key="64", text="64 \u00d7 64"),
            ft.DropdownOption(key="128", text="128 \u00d7 128"),
            ft.DropdownOption(key="256", text="256 \u00d7 256"),
            ft.DropdownOption(key="512", text="512 \u00d7 512"),
            ft.DropdownOption(key="1024", text="1024 \u00d7 1024"),
        ],
        on_select=lambda e: on_resolution(int(resolution_dd.value)),
    )

    threshold_slider = ft.Slider(
        value=threshold,
        min=0,
        max=255,
        divisions=255,
        label="{value}",
        expand=True,
        on_change=lambda e: on_threshold(int(threshold_slider.value)),
    )

    invert_switch = ft.Switch(
        label="Invert",
        value=invert,
        on_change=lambda e: on_invert(bool(invert_switch.value)),
    )

    return ft.Container(
        bgcolor=ft.Colors.GREY_900,
        border_radius=ft.BorderRadius.all(6),
        padding=ft.Padding.all(10),
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[resolution_dd, invert_switch],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            value="Threshold",
                            size=11,
                            color=ft.Colors.GREY_400,
                        ),
                        threshold_slider,
                    ],
                    spacing=2,
                ),
                source_row,
                action_row,
            ],
            spacing=10,
        ),
    )
