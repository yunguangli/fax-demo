# -*- coding: utf-8 -*-
"""
Flet 键盘事件示例
演示键盘快捷键和事件处理

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ✅ Flet 1.0+: 使用 page.on_keyboard_event 处理键盘事件
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动
  - 注：键盘事件 API 在 Flet 1.0+ 中保持稳定，无重大破坏性变更
"""

import flet as ft


def main(page: ft.Page):
    page.title = "键盘事件示例"
    page.window.width = 600
    page.window.height = 500

    # 显示区域
    key_display = ft.Text(value="按下任意键...", size=20)
    shortcut_display = ft.Text(value="", size=16, color=ft.Colors.BLUE)
    
    # 输入框示例
    input_field = ft.TextField(
        label="输入框（支持 Ctrl+A 全选, Ctrl+C 复制）",
        multiline=True,
        min_lines=3,
        max_lines=5,
    )

    # 快捷键提示
    shortcuts_info = ft.Column([
        ft.Text("快捷键说明:", weight=ft.FontWeight.BOLD),
        ft.Text("Ctrl+S: 保存"),
        ft.Text("Ctrl+N: 新建"),
        ft.Text("Ctrl+Q: 退出"),
        ft.Text("Escape: 清空"),
        ft.Text("方向键: 移动指示器"),
    ])

    # 移动指示器
    indicator = ft.Container(
        content=ft.Icon(ft.Icons.ARROW_RIGHT, color=ft.Colors.WHITE),
        bgcolor=ft.Colors.BLUE,
        width=30,
        height=30,
        border_radius=15,
        alignment=ft.Alignment.CENTER,
        left=100,
        top=100,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
    )

    indicator_container = ft.Container(
        content=ft.Stack([indicator], width=200, height=200),
        bgcolor=ft.Colors.GREY_100,
        border_radius=10,
        width=200,
        height=200,
    )

    def on_keyboard(e: ft.KeyboardEvent):
        # 显示按键信息
        modifiers = []
        if e.shift:
            modifiers.append("Shift")
        if e.ctrl:
            modifiers.append("Ctrl")
        if e.alt:
            modifiers.append("Alt")
        if e.meta:
            modifiers.append("Meta")
        
        modifier_str = " + ".join(modifiers) + " + " if modifiers else ""
        key_display.value = f"按键: {modifier_str}{e.key}"
        
        # 处理快捷键
        if e.ctrl and e.key == "S":
            shortcut_display.value = "执行: 保存"
            shortcut_display.color = ft.Colors.GREEN
        elif e.ctrl and e.key == "N":
            shortcut_display.value = "执行: 新建"
            shortcut_display.color = ft.Colors.GREEN
        elif e.ctrl and e.key == "Q":
            shortcut_display.value = "执行: 退出"
            shortcut_display.color = ft.Colors.RED
            page.window.close()
        elif e.key == "Escape":
            shortcut_display.value = "执行: 清空"
            shortcut_display.color = ft.Colors.ORANGE
            input_field.value = ""
        # 方向键移动
        elif e.key == "Arrow Up":
            indicator.top = max(0, indicator.top - 10)
            shortcut_display.value = "向上移动"
        elif e.key == "Arrow Down":
            indicator.top = min(170, indicator.top + 10)
            shortcut_display.value = "向下移动"
        elif e.key == "Arrow Left":
            indicator.left = max(0, indicator.left - 10)
            shortcut_display.value = "向左移动"
        elif e.key == "Arrow Right":
            indicator.left = min(170, indicator.left + 10)
            shortcut_display.value = "向右移动"
        else:
            shortcut_display.value = ""
        
        page.update()

    # 绑定键盘事件
    page.on_keyboard_event = on_keyboard

    page.add(
        ft.Text("键盘事件示例", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Row([
            ft.Column([
                key_display,
                shortcut_display,
                ft.Divider(),
                input_field,
            ], expand=True),
            ft.VerticalDivider(),
            ft.Column([
                shortcuts_info,
                ft.Divider(),
                ft.Text("方向键测试:"),
                indicator_container,
            ]),
        ], expand=True),
        ft.Text("提示: 点击页面任意位置后按键盘", color=ft.Colors.GREY_500),
    )


ft.run(main)
