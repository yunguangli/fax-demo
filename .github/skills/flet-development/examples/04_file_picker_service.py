# -*- coding: utf-8 -*-
"""
Flet 文件选择器服务化示例
演示 Flet 1.0+ 中 FilePicker 作为服务的使用方式

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: page.add(FilePicker())  →  Flet 1.0+: 不再生效
  - ✅ Flet 1.0+: FilePicker 必须注册到 page.services：page.services.append(file_picker)
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动（不是 ft.app）
  - ✅ Flet 1.0+: 事件处理器中必须用 async def + await asyncio.sleep()
"""

import flet as ft
import asyncio


def main(page: ft.Page):
    """文件选择器示例主函数"""
    page.title = "文件选择器示例"
    page.window.width = 600
    page.window.height = 400
    page.padding = 30
    
    # 结果显示区域
    selected_files_text = ft.Text(
        value="尚未选择文件",
        size=16,
        color=ft.Colors.GREY_600,
    )
    
    # ✅ 创建 FilePicker 并添加到 page.services（Flet 1.0+ 新方式）
    file_picker = ft.FilePicker()
    page.services.append(file_picker)
    
    # 异步选择文件函数
    async def pick_files(e):
        """选择文件"""
        try:
            # ✅ pick_files() 直接返回 list[FilePickerFile]，不是 result.files
            files = await file_picker.pick_files(
                allow_multiple=True,
                file_type=ft.FilePickerFileType.ANY,
            )
            
            if files:
                file_names = [f.name for f in files]
                selected_files_text.value = f"选择了 {len(file_names)} 个文件：\n" + "\n".join(file_names)
                selected_files_text.color = ft.Colors.GREEN
            else:
                selected_files_text.value = "未选择文件"
                selected_files_text.color = ft.Colors.GREY_600
            
            page.update()
        except Exception as ex:
            selected_files_text.value = f"选择文件时出错: {str(ex)}"
            selected_files_text.color = ft.Colors.RED
            page.update()
    
    async def pick_images(e):
        """选择图片"""
        try:
            # ✅ pick_files() 直接返回 list[FilePickerFile]
            files = await file_picker.pick_files(
                allow_multiple=False,
                file_type=ft.FilePickerFileType.IMAGE,
                dialog_title="选择图片",
            )
            
            if files:
                file = files[0]
                selected_files_text.value = f"选择了图片：{file.name}\n路径：{file.path}"
                selected_files_text.color = ft.Colors.BLUE
            else:
                selected_files_text.value = "未选择图片"
                selected_files_text.color = ft.Colors.GREY_600
            
            page.update()
        except Exception as ex:
            selected_files_text.value = f"选择图片时出错: {str(ex)}"
            selected_files_text.color = ft.Colors.RED
            page.update()
    
    async def save_file(e):
        """保存文件"""
        try:
            # ✅ save_file() 直接返回 str | None（路径字符串）
            path = await file_picker.save_file(
                file_name="my_document.txt",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["txt", "md", "py"],
            )
            
            if path:
                selected_files_text.value = f"保存到：{path}"
                selected_files_text.color = ft.Colors.GREEN
            else:
                selected_files_text.value = "取消保存"
                selected_files_text.color = ft.Colors.GREY_600
            
            page.update()
        except Exception as ex:
            selected_files_text.value = f"保存文件时出错: {str(ex)}"
            selected_files_text.color = ft.Colors.RED
            page.update()
    
    async def get_directory(e):
        """选择目录"""
        try:
            # ✅ get_directory_path() 直接返回 str | None（路径字符串）
            path = await file_picker.get_directory_path(
                dialog_title="选择文件夹",
            )
            
            if path:
                selected_files_text.value = f"选择了目录：{path}"
                selected_files_text.color = ft.Colors.BLUE
            else:
                selected_files_text.value = "未选择目录"
                selected_files_text.color = ft.Colors.GREY_600
            
            page.update()
        except Exception as ex:
            selected_files_text.value = f"选择目录时出错: {str(ex)}"
            selected_files_text.color = ft.Colors.RED
            page.update()
    
    # 按钮
    buttons = ft.Row(
        [
            ft.Button(
                content=ft.Row(
                    [ft.Icon(ft.Icons.FILE_OPEN), ft.Text("选择文件")],
                    spacing=8,
                ),
                on_click=lambda e: asyncio.create_task(pick_files(e)),
            ),
            ft.Button(
                content=ft.Row(
                    [ft.Icon(ft.Icons.IMAGE), ft.Text("选择图片")],
                    spacing=8,
                ),
                on_click=lambda e: asyncio.create_task(pick_images(e)),
            ),
            ft.Button(
                content=ft.Row(
                    [ft.Icon(ft.Icons.SAVE), ft.Text("保存文件")],
                    spacing=8,
                ),
                on_click=lambda e: asyncio.create_task(save_file(e)),
            ),
            ft.Button(
                content=ft.Row(
                    [ft.Icon(ft.Icons.FOLDER_OPEN), ft.Text("选择目录")],
                    spacing=8,
                ),
                on_click=lambda e: asyncio.create_task(get_directory(e)),
            ),
        ],
        wrap=True,
        spacing=10,
    )
    
    # 页面布局
    page.add(
        ft.Column(
            [
                ft.Text(
                    "文件选择器服务示例",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Flet 1.0+ FilePicker 作为服务使用",
                    size=14,
                    color=ft.Colors.GREY_600,
                ),
                ft.Divider(),
                buttons,
                ft.Divider(),
                ft.Text("选择结果：", weight=ft.FontWeight.BOLD),
                selected_files_text,
            ],
            spacing=15,
        )
    )


if __name__ == "__main__":
    ft.run(main)
