# -*- coding: utf-8 -*-
"""
Flet 基础应用示例
演示最基本的 Flet 应用结构和启动方式

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: ft.app(target=main)  →  Flet 1.0+: 报错 "missing required argument: 'target'"
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动应用
  - ✅ Flet 1.0+: 所有颜色使用 ft.Colors.XXX（大写 C），不能用 ft.colors.XXX（小写 s）
"""

import flet as ft


def main(page: ft.Page):
    """应用主函数"""
    # 页面基本设置
    page.title = "基础应用示例"
    page.window.width = 600
    page.window.height = 400
    page.padding = 20
    
    # 添加内容
    page.add(
        ft.Column(
            [
                ft.Text("Hello, Flet!", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("这是基础应用示例", size=16, color=ft.Colors.GREY_600),
                ft.Divider(),
                ft.Button(
                    content=ft.Text("点击我"),
                    on_click=lambda e: print("按钮被点击了！"),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


# 使用 ft.run() 启动应用
if __name__ == "__main__":
    ft.run(main)
