# -*- coding: utf-8 -*-
"""
Flet 图表绑定示例
演示简单的数据可视化

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ✅ Flet 1.0+: Flet 内置无图表控件，可用 Container 组合或 Canvas 自定义绘制
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动
  - ✅ Flet 1.0+: 颜色使用 ft.Colors.XXX（大写 C）
  - 注：图表绘制 API 在 Flet 1.0+ 中无破坏性变更
"""

import flet as ft
import flet.canvas as cv
import asyncio
import random


def main(page: ft.Page):
    page.title = "数据可视化示例"
    page.window.width = 700
    page.window.height = 600
    page.scroll = ft.ScrollMode.AUTO

    # 模拟数据
    chart_data = [
        {"label": "一月", "value": 65},
        {"label": "二月", "value": 85},
        {"label": "三月", "value": 45},
        {"label": "四月", "value": 92},
        {"label": "五月", "value": 78},
        {"label": "六月", "value": 60},
    ]

    # 柱状图容器（带Y轴）
    chart_height = 150
    y_axis_labels = ft.Column(
        list[ft.Control]([ft.Text(f"{i}", size=10, color=ft.Colors.GREY_600, width=25) for i in [100, 75, 50, 25, 0]]),
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        height=chart_height,
    )
    bar_chart = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY)
    bar_chart_with_axis = ft.Row(
        list[ft.Control]([
            y_axis_labels,
            ft.Column(
                list[ft.Control]([
                    bar_chart,
                    ft.Divider(height=1, color=ft.Colors.GREY_400),
                    ft.Row(
                        list[ft.Control]([ft.Text(str(d["label"]), size=10, width=45, text_align=ft.TextAlign.CENTER) for d in chart_data]),
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    ),
                ])
            ),
        ]),
        vertical_alignment=ft.CrossAxisAlignment.END
    )

    # 最大值（用于计算比例）
    max_value = max(d["value"] for d in chart_data)

    def create_bar_chart():
        bar_chart.controls.clear()
        for item in chart_data:
            height = (item["value"] / 100) * chart_height
            bar_chart.controls.append(
                ft.Container(
                    content=ft.Text(f"{item['value']}", size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.BLUE,
                    width=40,
                    height=height,
                    border_radius=ft.BorderRadius(top_left=5, top_right=5, bottom_left=0, bottom_right=0),
                    alignment=ft.Alignment.CENTER,
                    animate=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
                )
            )

    create_bar_chart()

    # 进度条图表
    progress_bars = ft.Column(spacing=10)
    
    progress_data = [
        {"label": "CPU 使用率", "value": 0.75, "color": ft.Colors.RED},
        {"label": "内存使用率", "value": 0.60, "color": ft.Colors.ORANGE},
        {"label": "磁盘使用率", "value": 0.45, "color": ft.Colors.GREEN},
        {"label": "网络带宽", "value": 0.85, "color": ft.Colors.BLUE},
    ]

    def create_progress_bars():
        progress_bars.controls.clear()
        for item in progress_data:
            progress_bars.controls.append(
                ft.Column([
                    ft.Row([
                        ft.Text(item["label"], width=100),
                        ft.Text(f"{int(item['value'] * 100)}%", width=40),
                    ]),
                    ft.ProgressBar(
                        value=item["value"],
                        bar_height=10,
                        color=item["color"],
                        bgcolor=ft.Colors.GREY_200,
                        width=300,
                    ),
                ])
            )
    
    create_progress_bars()

    # 实时数据更新
    is_updating = [False]
    
    async def toggle_realtime(e):
        is_updating[0] = not is_updating[0]
        realtime_btn.content = ft.Text("停止更新" if is_updating[0] else "实时更新")
        page.update()
        
        while is_updating[0]:
            # 更新进度条数据
            for item in progress_data:
                item["value"] = random.uniform(0.3, 1.0)
            create_progress_bars()
            
            # 更新柱状图数据
            for item in chart_data:
                item["value"] = random.randint(30, 100)
            create_bar_chart()
            draw_line_chart()
            
            page.update()
            await asyncio.sleep(1)

    # 圆形进度指示器
    circular_indicators = ft.Row(
        [
            ft.Column([
                ft.ProgressRing(value=0.7, width=60, height=60, color=ft.Colors.BLUE),
                ft.Text("70%"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.ProgressRing(value=0.5, width=60, height=60, color=ft.Colors.GREEN),
                ft.Text("50%"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.ProgressRing(value=0.3, width=60, height=60, color=ft.Colors.RED),
                ft.Text("30%"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.ProgressRing(value=None, width=60, height=60),  # 不确定进度
                ft.Text("加载中"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    # 使用 Canvas 绘制简单折线图（带刻度和数值）
    canvas = cv.Canvas(width=380, height=180)
    
    def draw_line_chart():
        canvas.shapes.clear()
        
        # 绘制区域参数
        left_margin, right_margin = 45, 20
        top_margin, bottom_margin = 20, 30
        plot_width = 380 - left_margin - right_margin
        plot_height = 180 - top_margin - bottom_margin
        
        # 绘制Y轴刻度线和标签
        for i, val in enumerate([100, 75, 50, 25, 0]):
            y = top_margin + (i / 4) * plot_height
            # 刻度线
            canvas.shapes.append(
                cv.Line(x1=left_margin, y1=y, x2=380 - right_margin, y2=y,
                       paint=ft.Paint(color=ft.Colors.GREY_200, stroke_width=1))
            )
            # 刻度值
            canvas.shapes.append(
                cv.Text(x=left_margin - 35, y=y - 6, value=str(val),
                       style=ft.TextStyle(size=9, color=ft.Colors.GREY_600))
            )
        
        # 绘制坐标轴
        canvas.shapes.append(
            cv.Line(x1=left_margin, y1=180 - bottom_margin, x2=380 - right_margin, y2=180 - bottom_margin,
                   paint=ft.Paint(color=ft.Colors.GREY_500, stroke_width=1.5))
        )
        canvas.shapes.append(
            cv.Line(x1=left_margin, y1=top_margin, x2=left_margin, y2=180 - bottom_margin,
                   paint=ft.Paint(color=ft.Colors.GREY_500, stroke_width=1.5))
        )
        
        # 绘制折线和数据点
        points = []
        x_step = plot_width / (len(chart_data) - 1)
        for i, item in enumerate(chart_data):
            x = left_margin + i * x_step
            y = 180 - bottom_margin - (item["value"] / 100) * plot_height
            points.append((x, y))
            
            # X轴标签
            canvas.shapes.append(
                cv.Text(x=x - 15, y=180 - bottom_margin + 8, value=item["label"][:2],
                       style=ft.TextStyle(size=9, color=ft.Colors.GREY_600))
            )
            
            # 数据点
            canvas.shapes.append(
                cv.Circle(x=x, y=y, radius=5,
                         paint=ft.Paint(color=ft.Colors.BLUE, style=ft.PaintingStyle.FILL))
            )
            # 数据值
            canvas.shapes.append(
                cv.Text(x=x - 10, y=y - 18, value=str(item["value"]),
                       style=ft.TextStyle(size=9, color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD))
            )
        
        # 连接折线
        path = cv.Path(
            paint=ft.Paint(color=ft.Colors.BLUE, stroke_width=2, style=ft.PaintingStyle.STROKE),
            elements=[
                cv.Path.MoveTo(x=points[0][0], y=points[0][1]),
            ] + [cv.Path.LineTo(x=px, y=py) for px, py in points[1:]],
        )
        canvas.shapes.append(path)
        
        page.update()
    
    draw_line_chart()

    realtime_btn = ft.Button(
        content=ft.Text("实时更新"),
        style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE, color=ft.Colors.WHITE),
        on_click=toggle_realtime,
    )

    page.add(
        ft.Text("数据可视化示例", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        
        ft.Text("柱状图 (使用 Container):", weight=ft.FontWeight.W_500),
        ft.Container(
            content=bar_chart_with_axis,
            bgcolor=ft.Colors.GREY_50,
            padding=ft.Padding(20, 15, 20, 5),
            border_radius=10,
        ),
        
        ft.Divider(),
        ft.Text("折线图 (使用 Canvas):", weight=ft.FontWeight.W_500),
        ft.Container(
            content=canvas,
            bgcolor=ft.Colors.GREY_50,
            border_radius=10,
            padding=15,
        ),
        
        ft.Divider(),
        ft.Text("进度条:", weight=ft.FontWeight.W_500),
        progress_bars,
        
        ft.Divider(),
        ft.Text("圆形进度指示器:", weight=ft.FontWeight.W_500),
        circular_indicators,
        
        ft.Divider(),
        realtime_btn,
        
        ft.Text("提示: 复杂图表可使用 plotly、matplotlib 等库生成图片后显示",
                size=12, color=ft.Colors.GREY_500),
    )


ft.run(main)
