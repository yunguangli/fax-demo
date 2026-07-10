# -*- coding: utf-8 -*-
"""
Flet 自定义绘制示例
演示 Canvas 控件的绘图功能

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: Dropdown 用 on_change  →  Flet 1.0+: 改用 on_select
  - ❌ Flet 0.x: PaintStyle 枚举  →  Flet 1.0+: 改用 PaintingStyle
  - ❌ Flet 0.x: Paint stroke_dash  →  Flet 1.0+: 改用 stroke_dash_pattern
  - ❌ Flet 0.x: Path 方法调用(move_to/line_to) → Flet 1.0+: 改用 elements 列表
  - ❌ Flet 0.x: Polygon 控件  →  Flet 1.0+: 改用 Path
  - ✅ Flet 1.0+: 推荐 import flet.canvas as cv 方式导入 Canvas 相关类
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动
"""

import flet as ft
import flet.canvas as cv
import math


def main(page: ft.Page):
    page.title = "自定义绘制示例"
    page.window.width = 700
    page.window.height = 600

    # 绘制类型选择
    draw_type = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="shapes", label="图形"),
            ft.Radio(value="text", label="文字"),
            ft.Radio(value="lines", label="线条"),
            ft.Radio(value="combined", label="组合"),
        ]),
        value="shapes",
        on_change=lambda e: update_canvas(),
    )

    # 颜色选择
    color_picker = ft.Dropdown(
        label="颜色",
        width=150,
        value="blue",
        options=[
            ft.DropdownOption(key="blue", text="蓝色"),
            ft.DropdownOption(key="red", text="红色"),
            ft.DropdownOption(key="green", text="绿色"),
            ft.DropdownOption(key="purple", text="紫色"),
            ft.DropdownOption(key="orange", text="橙色"),
        ],
        on_select=lambda e: update_canvas(),
    )

    # Canvas 画布
    canvas = cv.Canvas(
        width=600,
        height=400,
        resize_interval=10,
        on_resize=lambda e: print(f"Canvas resized: {e.width}x{e.height}"),
    )

    def update_canvas():
        canvas.shapes.clear()
        selected_color = color_picker.value
        
        color_map = {
            "blue": ft.Colors.BLUE,
            "red": ft.Colors.RED,
            "green": ft.Colors.GREEN,
            "purple": ft.Colors.PURPLE,
            "orange": ft.Colors.ORANGE,
        }
        color = color_map.get(selected_color, ft.Colors.BLUE)
        
        if draw_type.value == "shapes":
            # 绘制矩形
            canvas.shapes.append(
                ft.canvas.Rect(
                    x=50, y=50, width=100, height=80,
                    paint=ft.Paint(color=color, stroke_width=2, style=ft.PaintingStyle.STROKE),
                )
            )
            
            # 绘制填充矩形
            canvas.shapes.append(
                ft.canvas.Rect(
                    x=200, y=50, width=100, height=80,
                    paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
                )
            )
            
            # 绘制圆形
            canvas.shapes.append(
                ft.canvas.Circle(
                    x=100, y=200, radius=50,
                    paint=ft.Paint(color=color, stroke_width=3, style=ft.PaintingStyle.STROKE),
                )
            )
            
            # 绘制填充圆形
            canvas.shapes.append(
                ft.canvas.Circle(
                    x=250, y=200, radius=50,
                    paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
                )
            )
            
            # 绘制椭圆
            canvas.shapes.append(
                ft.canvas.Oval(
                    x=400, y=150, width=150, height=100,
                    paint=ft.Paint(color=color, stroke_width=2, style=ft.PaintingStyle.STROKE),
                )
            )
            
            # 绘制圆角矩形
            canvas.shapes.append(
                ft.canvas.Rect(
                    x=50, y=300, width=120, height=80,
                    border_radius=15,
                    paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
                )
            )
            
            # 绘制多边形 (使用 Path)
            canvas.shapes.append(
                ft.canvas.Path(
                    elements=[
                        ft.canvas.Path.MoveTo(450, 50),
                        ft.canvas.Path.LineTo(500, 100),
                        ft.canvas.Path.LineTo(480, 150),
                        ft.canvas.Path.LineTo(420, 150),
                        ft.canvas.Path.LineTo(400, 100),
                        ft.canvas.Path.Close(),
                    ],
                    paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
                )
            )
            
        elif draw_type.value == "text":
            # 绘制文字
            canvas.shapes.append(
                ft.canvas.Text(
                    x=50, y=50,
                    value="Flet Canvas 文字绘制",
                    style=ft.TextStyle(
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=color,
                    ),
                )
            )
            
            # 旋转文字
            canvas.shapes.append(
                ft.canvas.Text(
                    x=100, y=200,
                    value="旋转 30°",
                    style=ft.TextStyle(size=18, color=color),
                    rotate=math.radians(30),
                )
            )
            
            # 大文字
            canvas.shapes.append(
                ft.canvas.Text(
                    x=200, y=300,
                    value="CANVAS",
                    style=ft.TextStyle(
                        size=48,
                        weight=ft.FontWeight.BOLD,
                        color=color,
                    ),
                )
            )
            
        elif draw_type.value == "lines":
            # 绘制直线
            canvas.shapes.append(
                ft.canvas.Line(
                    x1=50, y1=50, x2=250, y2=150,
                    paint=ft.Paint(color=color, stroke_width=3),
                )
            )
            
            # 绘制虚线
            canvas.shapes.append(
                ft.canvas.Line(
                    x1=50, y1=200, x2=250, y2=300,
                    paint=ft.Paint(
                        color=color,
                        stroke_width=2,
                        stroke_dash_pattern=[10, 5],  # 虚线模式
                    ),
                )
            )
            
            # 绘制路径
            path = ft.canvas.Path(
                elements=[
                    ft.canvas.Path.MoveTo(300, 50),
                    ft.canvas.Path.LineTo(400, 100),
                    ft.canvas.Path.LineTo(350, 200),
                    ft.canvas.Path.LineTo(450, 150),
                    ft.canvas.Path.Close(),
                ],
                paint=ft.Paint(color=color, stroke_width=2, style=ft.PaintingStyle.STROKE),
            )
            canvas.shapes.append(path)
            
            # 绘制曲线
            arc = ft.canvas.Arc(
                x=400, y=250, width=150, height=150,
                start_angle=0, sweep_angle=math.pi * 1.5,
                paint=ft.Paint(color=color, stroke_width=3, style=ft.PaintingStyle.STROKE),
            )
            canvas.shapes.append(arc)
            
        elif draw_type.value == "combined":
            # 组合绘制
            # 背景渐变矩形
            canvas.shapes.append(
                ft.canvas.Rect(
                    x=50, y=50, width=200, height=150,
                    paint=ft.Paint(
                        color=color,
                        style=ft.PaintingStyle.FILL,
                    ),
                )
            )
            
            # 边框
            canvas.shapes.append(
                ft.canvas.Rect(
                    x=50, y=50, width=200, height=150,
                    paint=ft.Paint(
                        color=ft.Colors.WHITE,
                        stroke_width=3,
                        style=ft.PaintingStyle.STROKE,
                    ),
                )
            )
            
            # 文字叠加
            canvas.shapes.append(
                ft.canvas.Text(
                    x=80, y=110,
                    value="组合图形",
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                )
            )
            
            # 装饰圆
            canvas.shapes.append(
                ft.canvas.Circle(
                    x=400, y=125, radius=60,
                    paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
                )
            )
            canvas.shapes.append(
                ft.canvas.Circle(
                    x=400, y=125, radius=40,
                    paint=ft.Paint(color=ft.Colors.WHITE, style=ft.PaintingStyle.FILL),
                )
            )
            canvas.shapes.append(
                ft.canvas.Circle(
                    x=400, y=125, radius=20,
                    paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
                )
            )
            
            # 坐标轴
            canvas.shapes.append(
                ft.canvas.Line(
                    x1=50, y1=350, x2=550, y2=350,
                    paint=ft.Paint(color=ft.Colors.GREY_400, stroke_width=1),
                )
            )
            canvas.shapes.append(
                ft.canvas.Line(
                    x1=50, y1=250, x2=50, y2=350,
                    paint=ft.Paint(color=ft.Colors.GREY_400, stroke_width=1),
                )
            )
        
        page.update()

    # 初始绘制
    update_canvas()

    page.add(
        ft.Text("自定义绘制示例", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Row([draw_type, color_picker]),
        ft.Divider(),
        ft.Container(
            content=canvas,
            bgcolor=ft.Colors.GREY_50,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            padding=10,
        ),
        ft.Divider(),
        ft.Text("Canvas 绘制组件: Rect, Circle, Oval, Line, Arc, Path, Polygon, Text",
                size=12, color=ft.Colors.GREY_500),
    )


ft.run(main)
