# -*- coding: utf-8 -*-
"""
Flet 动画效果示例
演示各种动画效果和交互

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: animate 参数作用于 opacity/rotation/scale  →  Flet 1.0+: 无效
  - ✅ Flet 1.0+: 分别使用 container.animate_opacity、container.animate_rotation、container.animate_scale
  - ❌ Flet 0.x: ft.alignment.center  →  Flet 1.0+: 报错 "no attribute 'center'"
  - ✅ Flet 1.0+: 使用 ft.Alignment.CENTER
  - ✅ Flet 1.0+: 事件处理器延迟必须用 await asyncio.sleep()，不能用 page.wait() 或 time.sleep()
"""

import flet as ft
import asyncio
import math


def main(page: ft.Page):
    """动画示例主函数"""
    page.title = "动画效果示例"
    page.window.width = 800
    page.window.height = 600
    page.padding = 30
    
    # ===== 示例 1: 悬停动画 =====
    # 关键点：悬停事件处理器必须是 async def
    # Flet 1.0+ 使用 on_hover 事件，参数 e.data 是布尔类型（True/False）
    hover_container = ft.Container(
        content=ft.Text("悬停查看效果", size=20, weight=ft.FontWeight.BOLD),
        width=200,
        height=100,
        bgcolor=ft.Colors.BLUE_100,
        border_radius=10,
        animate=300,  # 300毫秒动画
        alignment=ft.Alignment.CENTER,
    )
    
    async def on_hover(e):
        # Flet 1.0+ 中 e.data 是布尔值 True/False（不是字符串 "true"/"false"）
        if e.data:  # 鼠标进入（e.data 为 True）
            hover_container.bgcolor = ft.Colors.BLUE_700
            hover_container.width = 250
            hover_container.height = 120
            hover_container.content = ft.Text(
                "悬停中!", 
                size=24, 
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD,
            )
            hover_container.shadow = ft.BoxShadow(
                spread_radius=2,
                blur_radius=15,
                color=ft.Colors.BLUE_200,
            )
        else:  # 鼠标离开（e.data 为 False）
            hover_container.bgcolor = ft.Colors.BLUE_100
            hover_container.width = 200
            hover_container.height = 100
            hover_container.content = ft.Text(
                "悬停查看效果",
                size=20,
                weight=ft.FontWeight.BOLD,
            )
            hover_container.shadow = None
        page.update()
    
    hover_container.on_hover = on_hover
    
    # ===== 示例 2: 点击缩放动画 =====
    # 关键点：延迟恢复必须用 asyncio.sleep()，不能用 page.run_task + page.wait()
    scale_container = ft.Container(
        content=ft.Icon(ft.Icons.FAVORITE, size=50, color=ft.Colors.RED),
        width=100,
        height=100,
        bgcolor=ft.Colors.RED_50,
        border_radius=50,
        alignment=ft.Alignment.CENTER,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
    )
    
    async def on_click_scale(e):
        # 缩小动画
        scale_container.scale = 0.8
        page.update()
        
        # 等待一段时间后恢复
        await asyncio.sleep(0.1)  # 100毫秒
        
        # 恢复动画
        scale_container.scale = 1.0
        page.update()
    
    scale_container.on_click = on_click_scale
    
    # ===== 示例 3: 颜色渐变动画 =====
    color_container = ft.Container(
        content=ft.Text("点击改变颜色", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        width=200,
        height=100,
        bgcolor=ft.Colors.PURPLE,
        border_radius=10,
        alignment=ft.Alignment.CENTER,
        animate=500,  # 500毫秒动画
    )
    
    colors = [
        ft.Colors.PURPLE,
        ft.Colors.BLUE,
        ft.Colors.GREEN,
        ft.Colors.ORANGE,
        ft.Colors.RED,
    ]
    color_index = [0]  # 使用列表存储可变状态
    
    async def on_click_color(e):
        color_index[0] = (color_index[0] + 1) % len(colors)
        color_container.bgcolor = colors[color_index[0]]
        page.update()
    
    color_container.on_click = on_click_color
    
    # ===== 示例 4: 旋转动画 =====
    # 关键点：使用 math.radians() 或直接用弧度，rotate 属性设置 animate_rotation
    rotation_container = ft.Container(
        content=ft.Icon(ft.Icons.REFRESH, size=40, color=ft.Colors.WHITE),
        width=80,
        height=80,
        bgcolor=ft.Colors.TEAL,
        border_radius=40,
        alignment=ft.Alignment.CENTER,
        animate_rotation=ft.Animation(800, ft.AnimationCurve.EASE_IN_OUT),
    )
    
    rotation_angle = [0]
    
    async def on_click_rotate(e):
        rotation_angle[0] += 360
        # 使用 math.radians 将角度转换为弧度
        rotation_container.rotate = math.radians(rotation_angle[0])
        page.update()
    
    rotation_container.on_click = on_click_rotate
    
    # ===== 示例 5: 位置移动动画 =====
    position_container = ft.Container(
        content=ft.Icon(ft.Icons.DIRECTIONS_RUN, size=30, color=ft.Colors.WHITE),
        width=60,
        height=60,
        bgcolor=ft.Colors.AMBER,
        border_radius=30,
        alignment=ft.Alignment.CENTER,
        animate=ft.Animation(400, ft.AnimationCurve.BOUNCE_OUT),
    )
    
    positions = [
        {"left": 0, "top": 0},
        {"left": 150, "top": 0},
        {"left": 150, "top": 100},
        {"left": 0, "top": 100},
    ]
    position_index = [0]
    
    async def on_click_position(e):
        position_index[0] = (position_index[0] + 1) % len(positions)
        pos = positions[position_index[0]]
        position_container.left = pos["left"]
        position_container.top = pos["top"]
        page.update()
    
    position_stack = ft.Stack(
        [
            ft.Container(
                width=210,
                height=160,
                border=ft.Border.all(2, ft.Colors.GREY_300),  # 使用 ft.Border.all()
                border_radius=10,
            ),
            position_container,
        ],
        width=210,
        height=160,
    )
    
    # ===== 示例 6: 透明度动画 =====
    # 关键点：opacity 动画需要设置 animate_opacity 属性
    opacity_container = ft.Container(
        content=ft.Text("淡入淡出", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        width=200,
        height=100,
        bgcolor=ft.Colors.INDIGO,
        border_radius=10,
        alignment=ft.Alignment.CENTER,
        opacity=1.0,
        animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_IN_OUT),  # 使用 animate_opacity
    )
    
    async def on_click_opacity(e):
        opacity_container.opacity = 0.2 if opacity_container.opacity == 1.0 else 1.0
        page.update()
    
    opacity_container.on_click = on_click_opacity
    
    # 页面布局
    page.add(
        ft.Column(
            [
                ft.Text(
                    "Flet 动画效果示例",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Divider(),
                
                # 第一行
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("悬停动画", weight=ft.FontWeight.BOLD),
                                hover_container,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            [
                                ft.Text("点击缩放", weight=ft.FontWeight.BOLD),
                                scale_container,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            [
                                ft.Text("颜色渐变", weight=ft.FontWeight.BOLD),
                                color_container,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=30,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                
                ft.Divider(),
                
                # 第二行
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("旋转动画 (点击)", weight=ft.FontWeight.BOLD),
                                rotation_container,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            [
                                ft.Text("位置移动 (点击)", weight=ft.FontWeight.BOLD),
                                position_stack,
                                ft.Button(
                                    content=ft.Text("移动"),
                                    on_click=on_click_position,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            [
                                ft.Text("透明度动画", weight=ft.FontWeight.BOLD),
                                opacity_container,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=30,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                
                ft.Divider(),
                
                # 提示信息
                ft.Container(
                    content=ft.Text(
                        "💡 提示: 将鼠标悬停或点击上面的卡片查看动画效果",
                        color=ft.Colors.GREY_600,
                        size=14,
                    ),
                    bgcolor=ft.Colors.BLUE_50,
                    padding=15,
                    border_radius=8,
                ),
            ],
            spacing=20,
        )
    )


if __name__ == "__main__":
    ft.run(main)
