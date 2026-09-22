"""Line panel: P2P transceiver controls (peer picker, Transmit, Hang up).

Pure view — reads LineViewModel state through `refresh()`; sync controls
(peer selection, turbo switch) are wired directly to VM commands, async
actions (transmit / hang up) are spawned callbacks from the Control layer.
"""

from __future__ import annotations

import flet as ft

from .components import spawn


class LinePanel(ft.Container):
    """A compact control strip shown on the Scan tab above the previews."""

    def __init__(self, line_vm, *, on_transmit, on_hangup) -> None:
        self._vm = line_vm

        self._peer_dd = ft.Dropdown(
            width=240,
            label="Peer",
            options=[],
            on_select=lambda e: (
                line_vm.select_peer(str(self._peer_dd.value))
                if self._peer_dd.value
                else None
            ),
        )
        self._transmit_btn = ft.FilledButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.SEND, size=18), ft.Text("Transmit")],
                spacing=8,
            ),
            on_click=lambda e: spawn(on_transmit),
        )
        self._hangup_btn = ft.Button(
            content=ft.Row(
                [ft.Icon(ft.Icons.CLOSE, size=18), ft.Text("Hang up")],
                spacing=8,
            ),
            on_click=lambda e: spawn(on_hangup),
        )
        self._turbo_switch = ft.Switch(
            label="Turbo",
            value=line_vm.turbo,
            on_change=lambda e: line_vm.set_turbo(bool(self._turbo_switch.value)),
        )
        self._state_text = ft.Text(
            value="",
            size=12,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREY_200,
        )
        self._status_text = ft.Text(
            value="",
            size=12,
            color=ft.Colors.GREY_400,
            expand=True,
        )

        super().__init__(
            bgcolor=ft.Colors.GREY_900,
            border_radius=ft.BorderRadius.all(6),
            padding=ft.Padding.all(10),
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Row(
                        controls=[
                            self._peer_dd,
                            self._transmit_btn,
                            self._hangup_btn,
                            self._turbo_switch,
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        wrap=True,
                    ),
                    ft.Row(
                        controls=[self._state_text, self._status_text],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
            ),
        )

    def refresh(self, *, can_transmit: bool) -> None:
        """Sync every widget from the ViewModel (called by fax_view)."""
        vm = self._vm
        known = {p.id for p in vm.peers}
        self._peer_dd.options = [
            ft.DropdownOption(key=p.id, text=f"{p.name}  ({p.host})")
            for p in vm.peers
        ]
        if vm.selected_id in known:
            self._peer_dd.value = vm.selected_id
        else:
            self._peer_dd.value = None

        idle = vm.is_idle
        self._peer_dd.disabled = not idle
        self._transmit_btn.disabled = not (can_transmit and idle and vm.selected_id)
        self._hangup_btn.disabled = idle
        self._turbo_switch.value = vm.turbo

        progress = vm.progress_label
        self._state_text.value = (
            f"{vm.state_label}  ·  {progress}" if progress else vm.state_label
        )
        self._status_text.value = vm.status
