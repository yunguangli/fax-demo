# -*- coding: utf-8 -*-
"""
Flet 剪贴板操作示例
演示复制、粘贴等剪贴板功能

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: page.clipboard 已弃用 → Flet 1.0+: 改用 ft.Clipboard() 类
  - ✅ Flet 1.0+: clipboard 操作必须用 async def + await（异步操作）
  - ✅ Flet 1.0+: clipboard.set(文本) 设置内容
  - ✅ Flet 1.0+: await clipboard.get() 获取内容
"""

import flet as ft
import asyncio


async def main(page: ft.Page):
    page.title = "剪贴板操作示例"
    page.window.width = 500
    page.window.height = 450

    # 创建剪贴板实例（Flet 1.0+: 使用 ft.Clipboard() 替代 page.clipboard）
    clipboard = ft.Clipboard()

    # 输入框
    copy_input = ft.TextField(
        label="要复制的内容",
        multiline=True,
        min_lines=3,
        max_lines=5,
        value="这是要复制到剪贴板的文本内容！\n支持多行文本。",
    )
    
    # 显示剪贴板内容
    paste_display = ft.TextField(
        label="粘贴的内容",
        multiline=True,
        min_lines=3,
        max_lines=5,
        read_only=True,
    )
    
    # 状态显示
    status_text = ft.Text(value="", size=14, color=ft.Colors.GREEN)

    async def on_copy(e):
        """复制到剪贴板"""
        if copy_input.value:
            await clipboard.set(copy_input.value)
            status_text.value = f"已复制 {len(copy_input.value)} 个字符"
            status_text.color = ft.Colors.GREEN
        else:
            status_text.value = "没有内容可复制"
            status_text.color = ft.Colors.RED
        page.update()

    async def on_paste(e):
        """从剪贴板粘贴"""
        content = await clipboard.get()
        if content:
            paste_display.value = content
            status_text.value = f"已粘贴 {len(content)} 个字符"
            status_text.color = ft.Colors.BLUE
        else:
            paste_display.value = ""
            status_text.value = "剪贴板为空"
            status_text.color = ft.Colors.ORANGE
        page.update()

    async def on_copy_from_paste(e):
        """从粘贴区复制"""
        if paste_display.value:
            await clipboard.set(paste_display.value)
            status_text.value = f"已复制粘贴区内容 {len(paste_display.value)} 个字符"
            status_text.color = ft.Colors.GREEN
        page.update()

    async def on_clear_clipboard(e):
        """清空剪贴板"""
        await clipboard.set("")
        status_text.value = "剪贴板已清空"
        status_text.color = ft.Colors.ORANGE
        page.update()

    # 快速复制按钮行
    quick_copy_buttons = ft.Row([
        ft.Button(
            content=ft.Text("复制邮箱"),
            on_click=lambda e: asyncio.create_task(quick_copy("example@email.com")),
        ),
        ft.Button(
            content=ft.Text("复制电话"),
            on_click=lambda e: asyncio.create_task(quick_copy("138-0000-0000")),
        ),
        ft.Button(
            content=ft.Text("复制地址"),
            on_click=lambda e: asyncio.create_task(quick_copy("北京市朝阳区xxx街道xxx号")),
        ),
    ])

    async def quick_copy(text):
        """快速复制预设文本"""
        await clipboard.set(text)
        status_text.value = f"已复制: {text}"
        status_text.color = ft.Colors.GREEN
        page.update()

    page.add(
        ft.Text("剪贴板操作示例", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        
        ft.Text("快速复制:", weight=ft.FontWeight.W_500),
        quick_copy_buttons,
        ft.Divider(),
        
        ft.Row([
            ft.Column([
                ft.Text("复制区域:", weight=ft.FontWeight.W_500),
                copy_input,
                ft.Button(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CONTENT_COPY, size=18),
                        ft.Text("复制到剪贴板"),
                    ]),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
                    on_click=on_copy,
                ),
            ], expand=True),
            ft.VerticalDivider(),
            ft.Column([
                ft.Text("粘贴区域:", weight=ft.FontWeight.W_500),
                paste_display,
                ft.Row([
                    ft.Button(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CONTENT_PASTE, size=18),
                            ft.Text("粘贴"),
                        ]),
                        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
                        on_click=on_paste,
                    ),
                    ft.Button(
                        content=ft.Text("复制此内容"),
                        on_click=on_copy_from_paste,
                    ),
                ]),
            ], expand=True),
        ], expand=True),
        
        ft.Divider(),
        ft.Row([
            status_text,
            ft.Button(
                content=ft.Text("清空剪贴板"),
                style=ft.ButtonStyle(bgcolor=ft.Colors.RED_100),
                on_click=on_clear_clipboard,
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    )

    # 监听键盘快捷键
    def on_keyboard(e: ft.KeyboardEvent):
        if e.ctrl and e.key == "C":
            asyncio.create_task(on_copy(None))
        elif e.ctrl and e.key == "V":
            asyncio.create_task(on_paste(None))
    
    page.on_keyboard_event = on_keyboard

ft.run(main)
