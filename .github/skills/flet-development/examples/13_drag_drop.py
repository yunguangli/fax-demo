# -*- coding: utf-8 -*-
"""
Flet 拖拽功能示例
演示 DragTarget 和 Draggable 控件的使用

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: DragTarget 事件中用 e.data 接受拖拽  →  Flet 1.0+: 改用 e.accept
  - ❌ Flet 0.x: Draggable 用 on_drag_end  →  Flet 1.0+: 改用 on_drag_complete
  - ✅ Flet 1.0+: on_accept 事件处理器中用 e.accept() 接受拖拽
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动
"""

import flet as ft


def main(page: ft.Page):
    page.title = "拖拽功能示例"
    page.window.width = 600
    page.window.height = 500

    # 源数据
    items = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"]
    
    # 结果显示
    result_text = ft.Text(value="拖拽项目到右侧区域", size=16)
    
    # 已接收的项目列表
    received_items = ft.Column(scroll=ft.ScrollMode.AUTO)

    def make_draggable(item_name: str, index: int):
        """创建可拖拽的项目"""
        
        def on_drag_start(e):
            e.control.content.opacity = 0.5
            e.control.update()
        
        def on_drag_complete(e):
            e.control.content.opacity = 1.0
            e.control.update()
        
        return ft.Draggable(
            group="fruits",
            content=ft.Container(
                content=ft.Text(item_name, size=14),
                bgcolor=ft.Colors.BLUE_100,
                padding=10,
                border_radius=5,
                width=100,
            ),
            content_when_dragging=ft.Container(
                content=ft.Text(item_name, size=14),
                bgcolor=ft.Colors.BLUE_50,
                padding=10,
                border_radius=5,
                opacity=0.5,
                width=100,
            ),
            on_drag_start=on_drag_start,
            on_drag_complete=on_drag_complete,
        )

    def make_drop_target():
        """创建放置目标区域"""
        
        def on_drag_accept(e):
            # Flet 1.0+: 使用 e.control 获取目标控件
            # 源控件通过 page.get_control(e.src_id) 获取
            src = page.get_control(e.src_id)
            if src and src.content and src.content.content:
                item_text = src.content.content.value
                
                # 添加到接收列表
                received_items.controls.append(
                    ft.Container(
                        content=ft.Text(item_text, size=14),
                        bgcolor=ft.Colors.GREEN_100,
                        padding=10,
                        border_radius=5,
                    )
                )
                result_text.value = f"已接收: {item_text}"
                
                # 更新目标区域样式
                e.control.content.bgcolor = ft.Colors.GREEN_200
                e.control.update()
                page.update()
        
        def on_drag_will_accept(e):
            # Flet 1.0+: 使用 e.accept 而非 e.data
            if e.accept:
                e.control.content.bgcolor = ft.Colors.BLUE_200
            else:
                e.control.content.bgcolor = ft.Colors.GREY_200
            e.control.update()
        
        def on_drag_leave(e):
            # Flet 1.0+: 使用 e.src_id 获取源控件 ID
            e.control.content.bgcolor = ft.Colors.GREY_100
            e.control.update()
        
        return ft.DragTarget(
            group="fruits",
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.DOWNLOAD, size=40, color=ft.Colors.GREY_400),
                    ft.Text("拖放到这里", color=ft.Colors.GREY_500),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.GREY_100,
                width=200,
                height=200,
                border_radius=10,
                alignment=ft.Alignment.CENTER,
            ),
            on_accept=on_drag_accept,
            on_will_accept=on_drag_will_accept,
            on_leave=on_drag_leave,
        )

    # 源项目列表
    source_items = ft.Column(
        [make_draggable(item, i) for i, item in enumerate(items)],
        spacing=10,
    )

    # 布局
    page.add(
        ft.Text("拖拽功能示例", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Row([
            ft.Column([
                ft.Text("可拖拽项目", size=14, weight=ft.FontWeight.W_500),
                source_items,
            ]),
            ft.VerticalDivider(),
            ft.Column([
                ft.Text("放置区域", size=14, weight=ft.FontWeight.W_500),
                make_drop_target(),
            ]),
            ft.VerticalDivider(),
            ft.Column([
                ft.Text("已接收项目", size=14, weight=ft.FontWeight.W_500),
                received_items,
            ], expand=True),
        ], expand=True),
        ft.Divider(),
        result_text,
    )


ft.run(main)
