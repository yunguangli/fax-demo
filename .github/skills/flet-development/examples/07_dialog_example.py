# -*- coding: utf-8 -*-
"""
Flet 对话框示例
演示 Flet 1.0+ 中对话框的新显示方式

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: page.bottom_sheet = xxx  →  Flet 1.0+: 已移除（page 无此属性）
  - ❌ Flet 0.x: page.snack_bar = xxx      →  Flet 1.0+: 已移除
  - ✅ Flet 1.0+: 须使用 page.overlay.append(控件) 并设置 open=True 来显示
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动（不是 ft.app）
"""

import flet as ft


def main(page: ft.Page):
    """对话框示例主函数"""
    page.title = "对话框示例"
    page.window.width = 700
    page.window.height = 600
    page.padding = 30
    
    # 结果显示
    result_text = ft.Text(
        value="点击按钮显示对话框",
        size=16,
        color=ft.Colors.GREY_600,
    )
    
    # ===== 示例 1: 简单提示对话框 =====
    def show_alert_dialog(e):
        """显示提示对话框"""
        
        def close_dialog(e):
            # ✅ Flet 1.0+ 使用 pop_dialog() 关闭
            page.pop_dialog()
        
        alert_dialog = ft.AlertDialog(
            title=ft.Text("提示"),
            content=ft.Text("这是一个简单的提示对话框。"),
            actions=[
                ft.Button(
                    content=ft.Text("确定"),
                    on_click=close_dialog,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        # ✅ Flet 1.0+ 使用 show_dialog() 显示
        page.show_dialog(alert_dialog)
        result_text.value = "显示了提示对话框"
        result_text.color = ft.Colors.BLUE
        page.update()
    
    # ===== 示例 2: 确认对话框 =====
    def show_confirm_dialog(e):
        """显示确认对话框"""
        
        def handle_confirm(e):
            page.pop_dialog()
            result_text.value = "✓ 用户点击了确认"
            result_text.color = ft.Colors.GREEN
            page.update()
        
        def handle_cancel(e):
            page.pop_dialog()
            result_text.value = "✗ 用户点击了取消"
            result_text.color = ft.Colors.RED
            page.update()
        
        confirm_dialog = ft.AlertDialog(
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.HELP_OUTLINE, color=ft.Colors.BLUE),
                    ft.Text("确认操作"),
                ]
            ),
            content=ft.Text("您确定要执行此操作吗？"),
            actions=[
                ft.Button(
                    content=ft.Text("取消"),
                    on_click=handle_cancel,
                ),
                ft.Button(
                    content=ft.Text("确认"),
                    on_click=handle_confirm,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE,
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.show_dialog(confirm_dialog)
        result_text.value = "显示了确认对话框"
        result_text.color = ft.Colors.BLUE
        page.update()
    
    # ===== 示例 3: 输入对话框 =====
    def show_input_dialog(e):
        """显示输入对话框"""
        
        input_field = ft.TextField(
            label="请输入内容",
            hint_text="在此输入...",
            autofocus=True,
        )
        
        def handle_submit(e):
            value = input_field.value
            page.pop_dialog()
            if value:
                result_text.value = f"✓ 输入内容: {value}"
                result_text.color = ft.Colors.GREEN
            else:
                result_text.value = "✗ 未输入内容"
                result_text.color = ft.Colors.ORANGE
            page.update()
        
        def handle_cancel(e):
            page.pop_dialog()
            result_text.value = "✗ 取消了输入"
            result_text.color = ft.Colors.RED
            page.update()
        
        input_dialog = ft.AlertDialog(
            title=ft.Text("输入信息"),
            content=input_field,
            actions=[
                ft.Button(
                    content=ft.Text("取消"),
                    on_click=handle_cancel,
                ),
                ft.Button(
                    content=ft.Text("提交"),
                    on_click=handle_submit,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE,
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.show_dialog(input_dialog)
        result_text.value = "显示了输入对话框"
        result_text.color = ft.Colors.BLUE
        page.update()
    
    # ===== 示例 4: 底部 Sheet =====
    # Flet 1.0+ BottomSheet 使用方式：添加到 page.overlay 并设置 open=True
    def show_bottom_sheet(e):
        """显示底部 Sheet"""
        
        def handle_close(e):
            bottom_sheet.open = False
            page.update()
        
        def handle_option_selected(option: str):
            bottom_sheet.open = False
            result_text.value = f"✓ 选择了: {option}"
            result_text.color = ft.Colors.GREEN
            page.update()
        
        bottom_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "选择操作",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Divider(),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SHARE),
                            title=ft.Text("分享"),
                            on_click=lambda e: handle_option_selected("分享"),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.COPY),
                            title=ft.Text("复制"),
                            on_click=lambda e: handle_option_selected("复制"),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.DELETE, color=ft.Colors.RED),
                            title=ft.Text("删除", color=ft.Colors.RED),
                            on_click=lambda e: handle_option_selected("删除"),
                        ),
                        ft.Divider(),
                        ft.Button(
                            content=ft.Text("取消"),
                            on_click=handle_close,
                            width=400,
                        ),
                    ],
                    tight=True,
                ),
                padding=20,
            ),
        )
        # ✅ Flet 1.0+ 将 BottomSheet 添加到 page.overlay
        page.overlay.append(bottom_sheet)
        bottom_sheet.open = True
        page.update()
        result_text.value = "显示了底部 Sheet"
        result_text.color = ft.Colors.BLUE
        page.update()
    
    # ===== 示例 5: SnackBar 提示 =====
    # Flet 1.0+ SnackBar 使用方式：添加到 page.overlay 并设置 open=True
    def show_snackbar(e):
        """显示 SnackBar"""
        snackbar = ft.SnackBar(
            content=ft.Text("这是一个 SnackBar 提示信息！"),
            action=ft.SnackBarAction(
                label="撤销",
                on_click=lambda e: print("撤销操作"),
            ),
            bgcolor=ft.Colors.GREY_800,
        )
        # ✅ Flet 1.0+ 将 SnackBar 添加到 page.overlay
        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()
        result_text.value = "显示了 SnackBar"
        result_text.color = ft.Colors.BLUE
        page.update()
    
    # 按钮组
    buttons = ft.Row(
        [
            ft.Button(
                content=ft.Row(
                    [ft.Icon(ft.Icons.INFO), ft.Text("提示对话框")],
                    spacing=8,
                ),
                on_click=show_alert_dialog,
            ),
            ft.Button(
                content=ft.Row(
                    [ft.Icon(ft.Icons.HELP), ft.Text("确认对话框")],
                    spacing=8,
                ),
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE,
                ),
                on_click=show_confirm_dialog,
            ),
            ft.Button(
                content=ft.Row(
                    [ft.Icon(ft.Icons.EDIT), ft.Text("输入对话框")],
                    spacing=8,
                ),
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.GREEN,
                ),
                on_click=show_input_dialog,
            ),
            ft.Button(
                content=ft.Row(
                    [ft.Icon(ft.Icons.MENU), ft.Text("底部 Sheet")],
                    spacing=8,
                ),
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.PURPLE,
                ),
                on_click=show_bottom_sheet,
            ),
            ft.Button(
                content=ft.Row(
                    [ft.Icon(ft.Icons.NOTIFICATIONS), ft.Text("SnackBar")],
                    spacing=8,
                ),
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.ORANGE,
                ),
                on_click=show_snackbar,
            ),
        ],
        wrap=True,
        spacing=10,
    )
    
    # 说明信息
    info_box = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Flet 1.0+ 对话框/BottomSheet/SnackBar API 变更",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                ),
                ft.Text("• AlertDialog 显示: page.show_dialog(dialog)"),
                ft.Text("• AlertDialog 关闭: page.pop_dialog()"),
                ft.Text("• BottomSheet: page.overlay.append(sheet) + sheet.open = True"),
                ft.Text("• SnackBar: page.overlay.append(snackbar) + snackbar.open = True"),
                ft.Text("• 不再使用: page.bottom_sheet / page.snack_bar 属性"),
            ]
        ),
        bgcolor=ft.Colors.BLUE_50,
        padding=15,
        border_radius=8,
    )
    
    # 页面布局
    page.add(
        ft.Column(
            [
                ft.Text(
                    "对话框示例",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Divider(),
                info_box,
                ft.Divider(),
                buttons,
                ft.Divider(),
                ft.Text("操作结果：", weight=ft.FontWeight.BOLD),
                result_text,
            ],
            spacing=15,
        )
    )


if __name__ == "__main__":
    ft.run(main)
