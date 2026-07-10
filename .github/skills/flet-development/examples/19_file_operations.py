# -*- coding: utf-8 -*-
"""
Flet 文件系统操作示例
演示文件读写、目录浏览等功能

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: page.add(FilePicker())  →  Flet 1.0+: 不再生效
  - ✅ Flet 1.0+: FilePicker 必须 page.services.append(file_picker) 注册后方可使用
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动
  - ✅ Flet 1.0+: 所有异步操作必须用 async def + await
"""

import flet as ft
import asyncio
import os


async def main(page: ft.Page):
    page.title = "文件系统操作示例"
    page.window.width = 650
    page.window.height = 550

    # 文件选择器
    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    # 结果显示
    result_text = ft.TextField(
        label="操作结果",
        multiline=True,
        min_lines=5,
        max_lines=10,
        read_only=True,
    )
    
    # 文件内容显示
    file_content = ft.TextField(
        label="文件内容",
        multiline=True,
        min_lines=5,
        max_lines=10,
    )
    
    # 当前选择的路径
    current_path = ft.Text(value="未选择路径", size=12, color=ft.Colors.GREY_500)

    async def pick_single_file(e):
        """选择单个文件"""
        files = await file_picker.pick_files(
            dialog_title="选择文件",
            allowed_extensions=["txt", "py", "md", "json"],
            allow_multiple=False,
        )
        if files:
            current_path.value = files[0].path
            result_text.value = f"文件名: {files[0].name}\n路径: {files[0].path}\n大小: {files[0].size} 字节"
        else:
            result_text.value = "未选择文件"
        page.update()

    async def pick_multiple_files(e):
        """选择多个文件"""
        files = await file_picker.pick_files(
            dialog_title="选择多个文件",
            allow_multiple=True,
        )
        if files:
            result_text.value = f"选择了 {len(files)} 个文件:\n"
            for f in files:
                result_text.value += f"  - {f.name} ({f.size} bytes)\n"
        else:
            result_text.value = "未选择文件"
        page.update()

    async def pick_directory(e):
        """选择目录"""
        dir_path = await file_picker.get_directory_path(
            dialog_title="选择目录",
        )
        if dir_path:
            current_path.value = dir_path
            # 列出目录内容
            try:
                items = os.listdir(dir_path)
                result_text.value = f"目录: {dir_path}\n\n内容 ({len(items)} 项):\n"
                for item in items[:20]:  # 最多显示 20 项
                    full_path = os.path.join(dir_path, item)
                    if os.path.isdir(full_path):
                        result_text.value += f"  📁 {item}/\n"
                    else:
                        result_text.value += f"  📄 {item}\n"
                if len(items) > 20:
                    result_text.value += f"  ... 还有 {len(items) - 20} 项"
            except Exception as ex:
                result_text.value = f"无法读取目录: {ex}"
        else:
            result_text.value = "未选择目录"
        page.update()

    async def save_file(e):
        """保存文件"""
        save_path = await file_picker.save_file(
            dialog_title="保存文件",
            file_name="new_file.txt",
            allowed_extensions=["txt"],
        )
        if save_path:
            current_path.value = save_path
            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(file_content.value or "# 新文件\n")
                result_text.value = f"文件已保存到:\n{save_path}"
            except Exception as ex:
                result_text.value = f"保存失败: {ex}"
        else:
            result_text.value = "取消保存"
        page.update()

    async def read_file(e):
        """读取当前路径的文件"""
        path = current_path.value
        if path and path != "未选择路径":
            try:
                with open(path, "r", encoding="utf-8") as f:
                    file_content.value = f.read()
                result_text.value = f"已读取文件: {path}"
            except Exception as ex:
                result_text.value = f"读取失败: {ex}"
        else:
            result_text.value = "请先选择一个文件"
        page.update()

    page.add(
        ft.Text("文件系统操作示例", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        
        ft.Text("文件选择操作:", weight=ft.FontWeight.W_500),
        ft.Row([
            ft.Button(
                content=ft.Row([
                    ft.Icon(ft.Icons.INSERT_DRIVE_FILE, size=18),
                    ft.Text("选择文件"),
                ]),
                on_click=pick_single_file,
            ),
            ft.Button(
                content=ft.Row([
                    ft.Icon(ft.Icons.FOLDER_OPEN, size=18),
                    ft.Text("选择目录"),
                ]),
                on_click=pick_directory,
            ),
            ft.Button(
                content=ft.Row([
                    ft.Icon(ft.Icons.LIBRARY_ADD, size=18),
                    ft.Text("多选文件"),
                ]),
                on_click=pick_multiple_files,
            ),
        ]),
        
        ft.Divider(),
        current_path,
        
        ft.Row([
            ft.Column([
                ft.Text("操作结果:", weight=ft.FontWeight.W_500),
                ft.Container(
                    content=result_text,
                    width=280,
                ),
            ]),
            ft.VerticalDivider(),
            ft.Column([
                ft.Text("文件内容:", weight=ft.FontWeight.W_500),
                file_content,
                ft.Row([
                    ft.Button(
                        content=ft.Text("读取文件"),
                        on_click=read_file,
                    ),
                    ft.Button(
                        content=ft.Row([
                            ft.Icon(ft.Icons.SAVE, size=18),
                            ft.Text("保存文件"),
                        ]),
                        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
                        on_click=save_file,
                    ),
                ]),
            ], expand=True),
        ], expand=True),
        
        ft.Divider(),
        ft.Text("注意: FilePicker 需要添加到 page.services", 
                size=12, color=ft.Colors.GREY_500),
    )


ft.run(main)
