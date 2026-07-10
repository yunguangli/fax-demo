# -*- coding: utf-8 -*-
"""
Flet 异步实时更新示例 - 数字时钟
演示如何使用 asyncio 实现可靠的实时更新

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: 使用 ft.app(target=main) 启动  →  Flet 1.0+: 报错
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动
  - ✅ Flet 1.0+: 事件处理器中延迟必须用 await asyncio.sleep()，不能用 time.sleep()
  - ✅ Flet 1.0+: 所有颜色使用 ft.Colors.XXX（大写 C）
"""

import flet as ft
import asyncio
from datetime import datetime


def main(page: ft.Page):
    """时钟应用主函数"""
    page.title = "数字时钟"
    page.window.width = 600
    page.window.height = 400
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    
    # 中文星期映射
    weekday_map = {
        0: "星期一",
        1: "星期二",
        2: "星期三",
        3: "星期四",
        4: "星期五",
        5: "星期六",
        6: "星期日",
    }
    
    # 创建显示控件
    clock_text = ft.Text(
        value="00:00:00",
        size=80,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_700,
    )
    
    date_text = ft.Text(
        value="",
        size=24,
        color=ft.Colors.GREY_600,
    )
    
    # 添加控件到页面
    page.add(
        ft.Column(
            [
                clock_text,
                ft.Container(height=20),  # 间距
                date_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    
    # 异步更新时钟
    async def update_clock():
        """每秒更新一次时钟"""
        while True:
            now = datetime.now()
            clock_text.value = now.strftime("%H:%M:%S")
            date_text.value = (
                f"{now.strftime('%Y年%m月%d日')} {weekday_map[now.weekday()]}"
            )
            page.update()
            await asyncio.sleep(1)  # 使用 await asyncio.sleep
    
    # 启动异步任务
    asyncio.create_task(update_clock())


if __name__ == "__main__":
    ft.run(main)
