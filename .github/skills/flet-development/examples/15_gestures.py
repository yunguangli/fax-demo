# -*- coding: utf-8 -*-
"""
Flet 手势识别示例
演示点击、双击、长按、缩放等手势

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: DragUpdateEvent 用 e.local_x/local_y  →  Flet 1.0+: 改用 e.local_position.x/y
  - ✅ Flet 1.0+: 使用 GestureDetector 的 on_tap、on_double_tap、on_long_press 等事件
  - ✅ Flet 1.0+: InteractiveViewer 用于缩放平移（scrollable 参数名可能有变更）
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动
"""

import flet as ft


def main(page: ft.Page):
    page.title = "手势识别示例"
    page.window.width = 900
    page.window.height = 640

    # 手势状态显示
    gesture_info = ft.Text(value="执行手势操作...", size=16)
    tap_count = ft.Text(value="点击次数: 0", size=14)

    counter = [0]  # 使用列表存储可变计数

    # 双击检测
    last_click_time = [0.0]

    def on_double_tap_area_click(e):
        import time
        current_time = time.time()
        if current_time - last_click_time[0] < 0.3:
            update_info("双击！")
            last_click_time[0] = 0
        else:
            last_click_time[0] = current_time
            # 延迟显示单击
            time.sleep(0.35)
            if last_click_time[0] == current_time:
                update_info("单击")

    # 点击区域
    tap_area = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.TOUCH_APP, size=40, color=ft.Colors.BLUE),
            ft.Text("点击 / 双击 / 长按"),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=ft.Colors.BLUE_50,
        width=200,
        height=120,
        border_radius=10,
        alignment=ft.Alignment.CENTER,
        ink=True,
        on_click=on_double_tap_area_click,
        on_long_press=lambda: update_info("长按"),
    )

    def update_info(text):
        gesture_info.value = f"手势: {text}"
        counter[0] += 1
        tap_count.value = f"点击次数: {counter[0]}"
        page.update()

    # GestureDetector 示例
    gesture_detector = ft.GestureDetector(
        on_tap=lambda e: update_info("GestureDetector: 点击"),
        on_double_tap=lambda e: update_info("GestureDetector: 双击"),
        on_long_press_start=lambda e: update_info("GestureDetector: 长按开始"),
        on_long_press_end=lambda e: update_info("GestureDetector: 长按结束"),
        on_pan_update=lambda e: update_info(f"GestureDetector: 拖动 ({e.local_position.x:.0f}, {e.local_position.y:.0f})"),
        drag_interval=50,
        content=ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.GESTURE, size=40, color=ft.Colors.GREEN),
                ft.Text("GestureDetector 区域"),
                ft.Text("支持点击/双击/长按/拖动", size=12, color=ft.Colors.GREY_500),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.GREEN_50,
            width=200,
            height=120,
            border_radius=10,
            alignment=ft.Alignment.CENTER,
        ),
    )

    # InteractiveViewer 缩放示例
    interactive_viewer = ft.InteractiveViewer(
        content=ft.Container(
            content=ft.Image(
                src="https://picsum.photos/300/200",
                fit=ft.BoxFit.CONTAIN,
                width=300,
                height=200,
            ),
            bgcolor=ft.Colors.GREY_200,
            padding=10,
        ),
        min_scale=0.5,
        max_scale=3.0,
        boundary_margin=ft.Margin.all(1000),
        expand=True,
        on_interaction_start=lambda e: update_info("开始交互"),
        on_interaction_end=lambda e: update_info("结束交互"),
        on_interaction_update=lambda e: update_info(f"缩放: {e.scale:.2f}x"),
    )

    # 水平滑动检测（带动效）
    swipe_offset = [0.0]  # 使用列表存储可变偏移量
    
    swipe_area = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.SWIPE, size=40, color=ft.Colors.PURPLE),
            ft.Text("水平滑动检测"),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=ft.Colors.PURPLE_50,
        width=200,
        height=80,
        border_radius=10,
        alignment=ft.Alignment.CENTER,
    )
    
    def on_swipe_start(e):
        swipe_area.bgcolor = ft.Colors.PURPLE_100
        swipe_area.update()
        update_info("开始水平滑动")
    
    def on_swipe_update(e):
        # 更新偏移量实现滑动动效
        swipe_offset[0] += e.primary_delta or 0
        swipe_area.offset = ft.Offset(swipe_offset[0] / 100, 0)
        swipe_area.update()
        update_info(f"水平滑动: {swipe_offset[0]:.1f}px")
    
    def on_swipe_end(e):
        swipe_area.bgcolor = ft.Colors.PURPLE_50
        # 复位动画
        swipe_offset[0] = 0
        swipe_area.offset = ft.Offset(0, 0)
        swipe_area.animate_offset = 300  # 300ms 复位动画
        swipe_area.update()
        update_info("水平滑动结束")
    
    swipe_detector = ft.Container(
        content=ft.GestureDetector(
            on_horizontal_drag_start=on_swipe_start,
            on_horizontal_drag_update=on_swipe_update,
            on_horizontal_drag_end=on_swipe_end,
            content=swipe_area,
        ),
        width=400,  # 更大的容器允许滑动
        height=100,
        alignment=ft.Alignment.CENTER,
    )

    page.add(
        ft.Text("手势识别示例", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Row([
            gesture_info,
            tap_count,
        ]),
        ft.Divider(),
        ft.Row([
            ft.Column([
                ft.Text("Container 手势:", weight=ft.FontWeight.W_500),
                tap_area,
            ]),
            ft.Column([
                ft.Text("GestureDetector:", weight=ft.FontWeight.W_500),
                gesture_detector,
            ]),
            ft.Column([
                ft.Text("滑动检测:", weight=ft.FontWeight.W_500),
                swipe_detector,
            ]),
        ], spacing=20),
        ft.Divider(),
        ft.Text("InteractiveViewer (缩放/平移):", weight=ft.FontWeight.W_500),
        # 使用 Row + expand=True 确保占满整行宽度
        ft.Row([
            ft.Container(
                content=interactive_viewer,
                bgcolor=ft.Colors.GREY_100,
                border_radius=10,
                padding=10,
                height=250,
                expand=True,
            ),
        ], expand=True),
    )


ft.run(main)
