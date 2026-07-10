# -*- coding: utf-8 -*-
"""
Flet 窗口控制示例
演示窗口尺寸、位置、状态等控制功能

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: page.on_resized 事件  →  Flet 1.0+: 事件名改为 on_resize
  - ✅ Flet 1.0+: 使用 page.on_resize 捕获窗口尺寸变化
  - ✅ Flet 1.0+: 使用 page.window 属性控制窗口（保持一致）
"""

import asyncio
import flet as ft


def main(page: ft.Page):
    """窗口控制示例主函数"""
    page.title = "窗口控制示例"
    page.window.width = 800
    page.window.height = 600
    
    # ===== 窗口状态显示 =====
    window_info = ft.Column()
    
    def update_window_info():
        """更新窗口信息显示"""
        window_info.controls = [
            ft.Text("窗口状态:", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"宽度: {page.window.width} px"),
            ft.Text(f"高度: {page.window.height} px"),
            ft.Text(f"位置 X: {page.window.left} px"),
            ft.Text(f"位置 Y: {page.window.top} px"),
            ft.Text(f"标题: {page.title}"),
            ft.Text(f"可调整大小: {page.window.resizable}"),
            ft.Text(f"可移动: {page.window.movable}"),
            ft.Text(f"始终置顶: {page.window.always_on_top}"),
            ft.Text(f"全屏: {page.window.full_screen}"),
            ft.Text(f"最大化: {page.window.maximized}"),
            ft.Text(f"最小化: {page.window.minimized}"),
            ft.Text(f"可见: {page.window.visible}"),
            # 注: Flet 1.0+ 中 transparent 属性已移除
            ft.Divider(),
            ft.Text("屏幕信息:", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"屏幕宽度: {page.window.max_width} px"),
            ft.Text(f"屏幕高度: {page.window.max_height} px"),
        ]
        page.update()
    
    # ✅ Flet 1.0+ 使用 on_resize 替代 on_resized
    def on_window_resize(e):
        """窗口大小变化事件"""
        update_window_info()
    
    page.on_resize = on_window_resize
    
    # ===== 窗口尺寸控制 =====
    size_input_width = ft.TextField(
        label="宽度",
        value=str(int(page.window.width or 800)),
        width=120,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    size_input_height = ft.TextField(
        label="高度",
        value=str(int(page.window.height or 600)),
        width=120,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    
    def resize_window(e):
        """调整窗口大小"""
        try:
            width = int(size_input_width.value)
            height = int(size_input_height.value)
            page.window.width = width
            page.window.height = height
            update_window_info()
        except ValueError:
            print("请输入有效的数字")
    
    # ===== 预设尺寸 =====
    def create_size_buttons():
        """创建预设尺寸按钮"""
        presets = [
            ("800x600", 800, 600),
            ("1024x768", 1024, 768),
            ("1280x720", 1280, 720),
            ("全屏", None, None),
        ]
        
        buttons = []
        for name, w, h in presets:
            buttons.append(
                ft.Button(
                    content=ft.Text(name, size=12),
                    on_click=lambda e, w=w, h=h: set_preset_size(w, h),
                )
            )
        return buttons
    
    def set_preset_size(width, height):
        """设置预设尺寸"""
        if width is None and height is None:
            page.window.full_screen = True
        else:
            page.window.full_screen = False
            page.window.width = width
            page.window.height = height
        update_window_info()
    
    # ===== 窗口状态控制 =====
    def create_state_buttons():
        """创建窗口状态按钮"""
        return ft.Column([
            ft.Text("窗口状态:", weight=ft.FontWeight.W_500),
            ft.Row([
                ft.Button(
                    content=ft.Row([ft.Icon(ft.Icons.CHECK_BOX_OUTLINE_BLANK), ft.Text("最大化")]),
                    on_click=lambda e: toggle_maximize(),
                ),
                ft.Button(
                    content=ft.Row([ft.Icon(ft.Icons.MINIMIZE), ft.Text("最小化")]),
                    on_click=lambda e: minimize_window(),
                ),
                ft.Button(
                    content=ft.Row([ft.Icon(ft.Icons.FULLSCREEN), ft.Text("全屏")]),
                    on_click=lambda e: toggle_fullscreen(),
                ),
            ], wrap=True, spacing=10),
            
            ft.Container(height=10),
            
            ft.Text("窗口属性:", weight=ft.FontWeight.W_500),
            ft.Row([
                ft.Button(
                    content=ft.Text("置顶"),
                    on_click=lambda e: toggle_always_on_top(),
                ),
                ft.Button(
                    content=ft.Text("禁止调整大小"),
                    on_click=lambda e: toggle_resizable(),
                ),
                ft.Button(
                    content=ft.Text("禁止移动"),
                    on_click=lambda e: toggle_movable(),
                ),
            ], wrap=True, spacing=10),
            
            ft.Container(height=10),
            
            ft.Text("危险操作:", weight=ft.FontWeight.W_500, color=ft.Colors.RED),
            ft.Row([
                ft.Button(
                    content=ft.Text("隐藏窗口"),
                    style=ft.ButtonStyle(color=ft.Colors.RED),
                    on_click=lambda e: hide_window(),
                ),
                ft.Button(
                    content=ft.Text("关闭窗口"),
                    style=ft.ButtonStyle(color=ft.Colors.RED),
                    on_click=lambda e: asyncio.create_task(close_window()),
                ),
            ], spacing=10),
        ])
    
    def toggle_maximize():
        """切换最大化"""
        page.window.maximized = not page.window.maximized
        update_window_info()
    
    def minimize_window():
        """最小化窗口"""
        page.window.minimized = True
        update_window_info()
    
    def toggle_fullscreen():
        """切换全屏"""
        page.window.full_screen = not page.window.full_screen
        update_window_info()
    
    def toggle_always_on_top():
        """切换始终置顶"""
        page.window.always_on_top = not page.window.always_on_top
        update_window_info()
    
    def toggle_resizable():
        """切换可调整大小"""
        page.window.resizable = not page.window.resizable
        update_window_info()
    
    def toggle_movable():
        """切换可移动"""
        page.window.movable = not page.window.movable
        update_window_info()
    
    def hide_window():
        """隐藏窗口"""
        page.window.visible = False
        # 3秒后显示
        import asyncio
        async def show_after_delay():
            await asyncio.sleep(3)
            page.window.visible = True
            update_window_info()
        asyncio.create_task(show_after_delay())
    
    async def close_window():
        """关闭窗口"""
        await page.window.close()
    
    # ===== 窗口位置控制 =====
    def create_position_buttons():
        """创建位置控制按钮"""
        return ft.Column([
            ft.Text("窗口位置:", weight=ft.FontWeight.W_500),
            ft.Row([
                ft.Button(content=ft.Text("居中"), on_click=lambda e: asyncio.create_task(center_window())),
                ft.Button(content=ft.Text("左上角"), on_click=lambda e: move_to_corner("top_left")),
                ft.Button(content=ft.Text("右下角"), on_click=lambda e: move_to_corner("bottom_right")),
            ], spacing=10),
        ])
    
    async def center_window():
        """窗口居中"""
        await page.window.center()
        update_window_info()
    
    def move_to_corner(corner: str):
        """移动到角落"""
        if corner == "top_left":
            page.window.left = 0
            page.window.top = 0
        elif corner == "bottom_right":
            # 屏幕尺寸可能为 None，使用默认值
            max_w = page.window.max_width or 1920
            max_h = page.window.max_height or 1080
            win_w = page.window.width or 800
            win_h = page.window.height or 600
            page.window.left = max_w - win_w
            page.window.top = max_h - win_h
        update_window_info()
    
    # ===== 标题栏控制 =====
    def create_title_section():
        """标题栏控制"""
        title_input = ft.TextField(
            label="窗口标题",
            value=page.title,
            width=300,
        )
        
        def change_title(e):
            page.title = title_input.value
            update_window_info()
        
        return ft.Column([
            ft.Text("窗口标题:", weight=ft.FontWeight.W_500),
            ft.Row([
                title_input,
                ft.Button(content=ft.Text("应用"), on_click=change_title),
            ], spacing=10),
        ])
    
    # ===== 透明窗口示例 =====
    def create_transparency_section():
        """透明窗口说明"""
        return ft.Container(
            content=ft.Column([
                ft.Text("透明窗口说明:", weight=ft.FontWeight.W_500),
                ft.Markdown("""
⚠️ **Flet 1.0+ 破坏性变更**: `page.window.transparent` 属性已移除

旧版本配置方式（已失效）：
- ❌ `page.window.transparent = True`
- ❌ `ft.run(main, transparent_window=True)`

新版本替代方案：
- 使用 `page.bgcolor = ft.Colors.TRANSPARENT` 配合特定平台配置
- 注意：透明窗口功能在 Flet 1.0+ 中可能有限制或平台差异
                """, selectable=True),
            ]),
            bgcolor=ft.Colors.GREY_100,
            padding=15,
            border_radius=10,
        )
    
    # ===== 页面布局 =====
    page.add(
        ft.Column([
            ft.Text(
                "窗口控制示例",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            ft.Text("演示 Flet 窗口的各种控制功能", color=ft.Colors.GREY_600),
            ft.Divider(),
            
            ft.Row([
                # 左侧 - 窗口状态
                ft.Container(
                    content=window_info,
                    bgcolor=ft.Colors.GREY_50,
                    padding=15,
                    border_radius=10,
                    width=250,
                ),
                
                ft.VerticalDivider(),
                
                # 右侧 - 控制面板
                ft.Column([
                    ft.Text("窗口尺寸:", weight=ft.FontWeight.W_500),
                    ft.Row([
                        size_input_width,
                        size_input_height,
                        ft.Button(content=ft.Text("应用"), on_click=resize_window),
                    ], spacing=10),
                    
                    ft.Row(create_size_buttons(), spacing=10),
                    ft.Divider(),
                    
                    create_state_buttons(),
                    ft.Divider(),
                    
                    create_position_buttons(),
                    ft.Divider(),
                    
                    create_title_section(),
                    ft.Divider(),
                    
                    create_transparency_section(),
                ], scroll=ft.ScrollMode.AUTO, expand=True),
            ], expand=True),
        ], expand=True)
    )
    
    # 初始化显示
    update_window_info()


if __name__ == "__main__":
    ft.run(main)
