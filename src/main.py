"""Fax machine simulator — full app entry point (Scan + Read).

Architecture: Control-View-ViewModel (MVVM)

    src/
    ├── main.py                 # ENTRY: full fax (Scan + Read) + Control wiring
    ├── fax_reader.py           # ENTRY: read-only standalone + Control wiring
    ├── models/
    │   ├── __init__.py
    │   ├── fax_document.py     # FaxDocument dataclass + JSON (de)serialization
    │   ├── scanner.py          # image → 1-bit packed bitmap (BOX avg per cell)
    │   └── receiver.py         # packed bitmap → base64 PNG for ft.Image
    ├── viewmodels/
    │   ├── __init__.py
    │   ├── fax_viewmodel.py    # scan/read state + commands (re-preview on param change)
    │   └── reader_viewmodel.py # read-only state + load command
    └── views/
        ├── __init__.py
        ├── components.py       # ImagePanel, StatusBar, ControlBar, spawn()
        ├── fax_view.py         # build_fax_view: side-by-side Scanned | Received
        └── reader_view.py      # build_reader_view: Load + single image

How it works
============

A real fax machine scans a document into a grid of black/white pixels and
transmits them over a phone line; the receiver prints them back onto paper.
This simulator mimics that pipeline in software, replacing the phone line
with a JSON file.

Scanner pipeline (models/scanner.py):

    source image (any size, any format)
        │  PIL Image.open + convert("L")           → grayscale
        ▼
    square grayscale image (center-cropped)
        │  PIL resize((W,H), Resampling.BOX)        → BOX filter averages all
        ▼                                          source pixels in each output
    WxH grid of average grayscale values            cell = exactly the spec's
        │  point(lambda p: 0 if p < threshold else 255, mode="1")
        ▼                                          "average grayscale per cell"
    WxH 1-bit image (mode "1": 0=black, 255=white)
        │  Image.tobytes()                          → packed 1 bit/pixel,
        ▼                                          MSB-first, row-major
    packed bitmap bytes
        │  base64.b64encode(...)                    → ASCII-safe for JSON
        ▼
    FaxDocument JSON: {"version":1,"width":W,"height":H,
                       "threshold":T,"invert":B,"data":"<base64>"}

Threshold direction: darker-than-threshold → black (conventional). The Invert
switch flips the comparison so bright pixels become black instead. Default
threshold = 128. Supported resolutions: 64 / 128 / 256 / 512 / 1024
(all widths are multiples of 8 so the packed bitmap has no row padding).

Receiver pipeline (models/receiver.py):

    JSON text
        │  json.loads + base64.b64decode            → packed bitmap bytes
        ▼
    Image.frombytes("1", (W,H), data)               → reconstructs the exact
        │                                          picture the scanner packed
        ▼
    PIL Image (mode "1", 0=black, 255=white)
        │  save(BytesIO, format="PNG") + base64     → single PNG string
        ▼
    ft.Image(src=base64_png)                         → ONE control renders the
                                                   entire image at any size.

Key design choice: never create one Flet control per pixel. A 1024x1024 fax
would mean ~1M Container widgets and freeze the UI. Instead, the whole fax is
decoded into one PIL Image and displayed via a single ft.Image control.

MVVM data flow:

    User clicks button
        │  Control layer (this file): async handler runs FilePicker/Camera
        ▼
    FilePicker / Camera returns bytes or path
        │  ViewModel.on_source_selected / load_fax_from_text
        ▼
    Model layer runs scan() or render_png_b64()
        │  ViewModel updates its state fields, calls _notify()
        ▼
    View's on_changed callback fires
        │  reads VM state, updates ImagePanel/StatusBar controls, page.update()
        ▼
    User sees updated Scanned preview | Received image

Re-preview on parameter change: when the user drags the threshold slider or
toggles Invert after a scan, the ViewModel re-runs scan_from_bytes() on the
cached source bytes (no disk re-read). This makes the threshold slider feel
live. Resolution changes also trigger a re-scan because the cell grid changes.

Run:
    uv run flet run            # desktop
    uv run flet run --web      # web
    uv run flet run src/fax_reader.py   # reader only
"""

from __future__ import annotations

import asyncio

import flet as ft

from viewmodels import FaxViewModel
from views import build_fax_view
from views.components import spawn


async def main(page: ft.Page) -> None:
    page.title = "Fax Machine"
    page.padding = 16
    page.bgcolor = ft.Colors.GREY_900
    page.theme_mode = ft.ThemeMode.DARK

    vm = FaxViewModel()

    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    # ---- Control-layer async handlers (bridge FilePicker/Camera -> VM) ----

    async def on_scan() -> None:
        try:
            fp = ft.FilePicker()
            files = await fp.pick_files(
                dialog_title="Pick an image to scan",
                file_type=ft.FilePickerFileType.IMAGE,
                allow_multiple=False,
            )
        except Exception as ex:
            vm.set_status(f"File picker failed: {type(ex).__name__}: {ex}")
            return
        if not files:
            vm.set_status("Load cancelled.")
            return
        f = files[0]
        if f.path:
            vm.on_source_selected(image_path=f.path)
        else:
            vm.set_status("Scan failed: no file path.")

    async def on_scan_run() -> None:
        # Process the already-loaded source image into a fax.
        vm.scan()

    async def on_save() -> None:
        json_text = vm.export_json()
        if json_text is None:
            return
        src_bytes = json_text.encode("utf-8")
        try:
            path = await file_picker.save_file(
                dialog_title="Save fax as JSON",
                file_name="fax.json",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["json"],
                src_bytes=src_bytes,
            )
        except Exception as ex:
            vm.set_status(f"File picker failed: {ex}")
            return
        if not path:
            vm.set_status("Save cancelled.")
            return
        # On desktop, save_file returns path but doesn't write the file
        if not page.web:
            try:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(json_text)
            except OSError as ex:
                vm.set_status(f"Save failed: {ex}")
                return
        vm.set_status(f"Saved to {path}")

    async def on_load() -> None:
        try:
            files = await file_picker.pick_files(
                dialog_title="Pick a fax JSON file",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["json"],
                allow_multiple=False,
            )
        except Exception as ex:
            vm.set_status(f"File picker failed: {ex}")
            return
        if not files:
            vm.set_status("Load cancelled.")
            return
        f = files[0]
        if f.path:
            try:
                with open(f.path, "r", encoding="utf-8") as fh:
                    vm.load_fax_from_text(fh.read())
            except OSError as ex:
                vm.set_status(f"Load failed: {ex}")
        else:
            vm.set_status("Load failed: no file path.")

    # ---- Camera ----
    # Camera MUST be in the visual tree (Stack in page controls) to work on web.
    import flet_camera as fc

    _camera: fc.Camera | None = None
    _camera_ready = False

    # Camera preview area
    _camera_stack = ft.Stack(controls=[], height=320)

    _capture_btn = ft.FilledButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.PHOTO_CAMERA, size=18), ft.Text("Capture")],
            spacing=8,
        ),
        on_click=lambda e: spawn(_on_camera_do_capture),
    )
    _cancel_btn = ft.Button(
        content=ft.Row(
            [ft.Icon(ft.Icons.CLOSE, size=18), ft.Text("Cancel")],
            spacing=8,
        ),
        on_click=lambda e: _on_camera_cancel(),
    )
    _retake_btn = ft.FilledButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.REFRESH, size=18), ft.Text("Retake")],
            spacing=8,
        ),
        on_click=lambda e: spawn(_on_camera_retake),
    )
    _done_btn = ft.Button(
        content=ft.Row(
            [ft.Icon(ft.Icons.CHECK, size=18), ft.Text("Done")],
            spacing=8,
        ),
        on_click=lambda e: _on_camera_cancel(),
    )

    # Two button rows: capture/cancel (during preview) and retake/done (after capture)
    _camera_btns_capture = ft.Row(
        controls=[_capture_btn, _cancel_btn],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
    )
    _camera_btns_retake = ft.Row(
        controls=[_retake_btn, _done_btn],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
        visible=False,
    )
    _camera_area = ft.Column(
        controls=[_camera_stack, _camera_btns_capture, _camera_btns_retake],
        spacing=8,
        visible=False,
        expand=False,
    )

    def _create_camera() -> fc.Camera:
        return fc.Camera(
            expand=True,
            preview_enabled=True,
            content=ft.Container(
                alignment=ft.Alignment.CENTER,
                content=ft.Icon(
                    ft.Icons.CENTER_FOCUS_STRONG,
                    color=ft.Colors.WHITE_70,
                    size=48,
                ),
            ),
        )

    async def _init_camera() -> bool:
        """Create a fresh Camera, mount it, and initialize it."""
        nonlocal _camera_ready, _camera
        # Tear down old camera
        _camera_stack.controls.clear()
        _camera = None
        _camera_ready = False
        # Create fresh camera
        _camera = _create_camera()
        _camera_stack.controls.append(_camera)
        _camera_area.visible = True
        _camera_area.update()
        await asyncio.sleep(0.3)
        devices: list[fc.CameraDescription] = []
        try:
            devices = await _camera.get_available_cameras()
        except Exception:
            pass
        init_kwargs = dict(
            resolution_preset=fc.ResolutionPreset.MEDIUM,
            enable_audio=False,
            image_format_group=fc.ImageFormatGroup.JPEG,
        )
        try:
            if devices:
                await _camera.initialize(description=devices[0], **init_kwargs)
            else:
                await _camera.initialize(**init_kwargs)
        except Exception as ex:
            vm.set_status(f"Camera init failed: {ex}")
            _hide_camera_area()
            return False
        _camera_ready = True
        return True

    def _hide_camera_area() -> None:
        _camera_area.visible = False
        _camera_area.update()

    def _show_camera_area() -> None:
        _camera_area.visible = True
        _camera_area.update()

    def _on_camera_cancel() -> None:
        _hide_camera_area()
        vm.set_status("Camera cancelled.")
        page.update()

    async def _on_camera_do_capture() -> None:
        if _camera is None:
            return
        try:
            data = await _camera.take_picture()
        except Exception as ex:
            vm.set_status(f"Camera capture failed: {ex}")
            return
        if not data:
            vm.set_status("Camera capture returned no data.")
            return
        # Send directly to ViewModel — shows in Original tab
        vm.on_source_selected(image_bytes=data, image_path="(camera)")
        # Switch buttons: hide capture/cancel, show retake/done
        _camera_btns_capture.visible = False
        _camera_btns_retake.visible = True
        _camera_area.update()

    async def _on_camera_retake() -> None:
        # Camera is still active — just switch buttons back to capture mode
        _camera_btns_retake.visible = False
        _camera_btns_capture.visible = True
        _camera_area.update()

    async def _open_camera_preview() -> None:
        ready = await _init_camera()
        if not ready:
            vm.set_status("Camera is not available on this platform.")
            return
        _camera_btns_retake.visible = False
        _camera_btns_capture.visible = True
        _show_camera_area()
        vm.set_status("Camera ready — frame and capture.")
        page.update()

    async def on_camera_button() -> None:
        await _open_camera_preview()

    extra_buttons: list = []
    extra_buttons.append(
        ft.FilledButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.PHOTO_CAMERA, size=18), ft.Text("Camera")],
                spacing=8,
            ),
            on_click=lambda e: spawn(on_camera_button),
        )
    )

    # ---- Build view and add to page ----
    view = build_fax_view(
        page,
        vm,
        on_scan=on_scan,
        on_scan_run=on_scan_run,
        on_save=on_save,
        on_load=on_load,
        extra_buttons=extra_buttons or None,
    )

    # Camera stack sits below the main view — invisible until user clicks Camera
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[_camera_area, view],
                expand=True,
                spacing=0,
            ),
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
