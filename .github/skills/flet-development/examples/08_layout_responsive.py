# -*- coding: utf-8 -*-
"""
Flet 布局与自适应示例
演示 Row、Column、Stack、expand、scroll 等布局功能

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: ft.alignment.center  →  Flet 1.0+: 报错 "no attribute 'center'"
  - ✅ Flet 1.0+: 使用 ft.Alignment.CENTER（大写 A）
  - ❌ Flet 0.x: ft.Badge(label_style=...) 或 ft.Badge(small=True)  →  Flet 1.0+: 报错
  - ✅ Flet 1.0+: Badge 只能使用 ft.Badge(label="文字")
  - ✅ Flet 1.0+: TabBarView 必须设置 height 属性，否则 "height is unbounded"
"""

import flet as ft


def main(page: ft.Page):
    """布局示例主函数"""
    page.title = "布局与自适应示例"
    page.window.width = 900
    page.window.height = 700
    page.padding = 20
    
    # ===== 1. Row 和 Column 布局 =====
    def create_layout_section():
        """基础行列布局"""
        return ft.Column([
            ft.Text("1. Row 和 Column 布局", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            # Row 水平布局
            ft.Text("Row（水平布局）:", weight=ft.FontWeight.W_500),
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text("项目 1", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.BLUE,
                        padding=20,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Container(
                        content=ft.Text("项目 2", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN,
                        padding=20,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Container(
                        content=ft.Text("项目 3", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.ORANGE,
                        padding=20,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,  # 主轴对齐
                vertical_alignment=ft.CrossAxisAlignment.CENTER,  # 交叉轴对齐
                spacing=10,  # 间距
            ),
            
            ft.Container(height=15),
            
            # Column 垂直布局
            ft.Text("Column（垂直布局）:", weight=ft.FontWeight.W_500),
            ft.Column(
                [
                    ft.Container(
                        content=ft.Text("上", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.PURPLE,
                        padding=15,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Container(
                        content=ft.Text("中", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.PINK,
                        padding=15,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Container(
                        content=ft.Text("下", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.CYAN,
                        padding=15,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                scroll=ft.ScrollMode.AUTO,  # 自动滚动
                height=150,
            ),
        ])
    
    # ===== 2. expand 自适应 =====
    def create_expand_section():
        """expand 自适应大小"""
        return ft.Column([
            ft.Text("2. expand 自适应", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.Text("使用 expand=True 让控件填充可用空间:", color=ft.Colors.GREY_700),
            
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Text("expand=1", color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.RED_400,
                            padding=20,
                            border_radius=8,
                            expand=1,  # 占 1 份
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Container(
                            content=ft.Text("expand=2", color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.BLUE_400,
                            padding=20,
                            border_radius=8,
                            expand=2,  # 占 2 份
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Container(
                            content=ft.Text("expand=1", color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.GREEN_400,
                            padding=20,
                            border_radius=8,
                            expand=1,  # 占 1 份
                            alignment=ft.Alignment.CENTER,
                        ),
                    ],
                    spacing=10,
                ),
                border=ft.Border.all(1, ft.Colors.GREY_300),
                border_radius=10,
                padding=10,
            ),
            
            ft.Container(height=10),
            
            ft.Text("垂直方向 expand:", color=ft.Colors.GREY_700),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Container(
                                        content=ft.Text("上", color=ft.Colors.WHITE),
                                        bgcolor=ft.Colors.INDIGO,
                                        padding=15,
                                        border_radius=8,
                                        alignment=ft.Alignment.CENTER,
                                    ),
                                    ft.Container(
                                        content=ft.Text("expand=True", color=ft.Colors.WHITE),
                                        bgcolor=ft.Colors.TEAL,
                                        padding=15,
                                        border_radius=8,
                                        alignment=ft.Alignment.CENTER,
                                        expand=True,  # 填充剩余空间
                                    ),
                                ],
                                spacing=5,
                            ),
                            expand=1,
                        ),
                        ft.Container(
                            content=ft.Text("固定宽度", color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.AMBER,
                            padding=20,
                            border_radius=8,
                            alignment=ft.Alignment.CENTER,
                            width=120,
                        ),
                    ],
                    spacing=10,
                    expand=True,
                ),
                height=200,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                border_radius=10,
                padding=10,
            ),
        ])
    
    # ===== 3. Stack 层叠布局 =====
    def create_stack_section():
        """Stack 层叠布局"""
        return ft.Column([
            ft.Text("3. Stack 层叠布局", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.Stack(
                [
                    # 底层 - 背景卡片
                    ft.Container(
                        width=300,
                        height=150,
                        bgcolor=ft.Colors.BLUE_100,
                        border_radius=15,
                    ),
                    # 中层 - 图片
                    ft.Container(
                        content=ft.Icon(ft.Icons.PEOPLE, size=60, color=ft.Colors.BLUE_300),
                        left=20,
                        top=20,
                    ),
                    # 顶层 - 文字
                    ft.Container(
                        content=ft.Column([
                            ft.Text("卡片标题", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text("这是卡片描述文字", color=ft.Colors.GREY_700),
                        ]),
                        left=100,
                        top=30,
                    ),
                    # 右上角徽章（使用 Container + Text 替代 Badge）
                    ft.Container(
                        content=ft.Text(
                            "新",
                            color=ft.Colors.WHITE,
                            size=12,
                            weight=ft.FontWeight.BOLD,
                        ),
                        bgcolor=ft.Colors.RED,
                        border_radius=10,
                        padding=ft.Padding(left=8, right=8, top=4, bottom=4),
                        right=10,
                        top=10,
                    ),
                ],
                width=300,
                height=150,
            ),
        ])
    
    # ===== 4. ResponsiveRow 响应式布局 =====
    def create_responsive_section():
        """ResponsiveRow 响应式布局"""
        return ft.Column([
            ft.Text("4. ResponsiveRow 响应式布局", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.Text(
                "根据屏幕宽度自动调整列数（调整窗口大小查看效果）",
                color=ft.Colors.GREY_700,
                size=12,
            ),
            
            ft.ResponsiveRow(
                [
                    ft.Container(
                        content=ft.Text("col={sm:6, md:4, lg:3}", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.BLUE,
                        padding=20,
                        border_radius=8,
                        col={"sm": 6, "md": 4, "lg": 3},  # 响应式列宽
                    ),
                    ft.Container(
                        content=ft.Text("col={sm:6, md:4, lg:3}", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN,
                        padding=20,
                        border_radius=8,
                        col={"sm": 6, "md": 4, "lg": 3},
                    ),
                    ft.Container(
                        content=ft.Text("col={sm:6, md:4, lg:3}", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.ORANGE,
                        padding=20,
                        border_radius=8,
                        col={"sm": 6, "md": 4, "lg": 3},
                    ),
                    ft.Container(
                        content=ft.Text("col={sm:6, md:4, lg:3}", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.PURPLE,
                        padding=20,
                        border_radius=8,
                        col={"sm": 6, "md": 4, "lg": 3},
                    ),
                    ft.Container(
                        content=ft.Text("col=6 (固定)", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.RED,
                        padding=20,
                        border_radius=8,
                        col=6,  # 固定占 6 列（总共 12 列）
                    ),
                    ft.Container(
                        content=ft.Text("col=6 (固定)", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.TEAL,
                        padding=20,
                        border_radius=8,
                        col=6,
                    ),
                ],
                spacing=10,
                run_spacing=10,  # 换行时的间距
            ),
            
            ft.Container(height=10),
            
            ft.Text("响应式断点说明:", weight=ft.FontWeight.W_500),
            ft.Text("sm < 576px | md >= 576px | lg >= 768px | xl >= 992px | xxl >= 1200px", 
                   color=ft.Colors.GREY_600, size=12),
        ])
    
    # ===== 5. 滚动控制 =====
    def create_scroll_section():
        """滚动控制"""
        return ft.Column([
            ft.Text("5. 滚动控制", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.Row([
                # ScrollMode.ADAPTIVE - 自动显示滚动条
                ft.Column([
                    ft.Text("ADAPTIVE", weight=ft.FontWeight.W_500, size=12),
                    ft.Container(
                        content=ft.ListView(
                            [ft.Text(f"项目 {i}") for i in range(20)],
                            scroll=ft.ScrollMode.ADAPTIVE,  # 自适应滚动
                        ),
                        width=150,
                        height=150,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                    ),
                ]),

                # ScrollMode.AUTO - 内容溢出时滚动
                ft.Column([
                    ft.Text("AUTO", weight=ft.FontWeight.W_500, size=12),
                    ft.Container(
                        content=ft.ListView(
                            [ft.Text(f"项目 {i}") for i in range(20)],
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        width=150,
                        height=150,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                    ),
                ]),

                # ScrollMode.HIDDEN - 隐藏滚动条
                ft.Column([
                    ft.Text("HIDDEN", weight=ft.FontWeight.W_500, size=12),
                    ft.Container(
                        content=ft.ListView(
                            [ft.Text(f"项目 {i}") for i in range(20)],
                            scroll=ft.ScrollMode.HIDDEN,
                        ),
                        width=150,
                        height=150,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                    ),
                ]),

                # ScrollMode.ALWAYS - 始终显示滚动条
                ft.Column([
                    ft.Text("ALWAYS", weight=ft.FontWeight.W_500, size=12),
                    ft.Container(
                        content=ft.ListView(
                            [ft.Text(f"项目 {i}") for i in range(20)],
                            scroll=ft.ScrollMode.ALWAYS,
                        ),
                        width=150,
                        height=150,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                    ),
                ]),
            ], spacing=20),
        ])
    
    # ===== 6. GridView 网格布局 =====
    def create_grid_section():
        """GridView 网格布局"""
        return ft.Column([
            ft.Text("6. GridView 网格布局", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.GridView(
                [
                    ft.Container(
                        content=ft.Text(f"{i}", size=20, color=ft.Colors.WHITE),
                        bgcolor=[
                            ft.Colors.BLUE,
                            ft.Colors.GREEN,
                            ft.Colors.ORANGE,
                            ft.Colors.PURPLE,
                            ft.Colors.RED,
                            ft.Colors.TEAL,
                            ft.Colors.CYAN,
                            ft.Colors.INDIGO,
                            ft.Colors.PINK,
                            ft.Colors.AMBER,
                            ft.Colors.LIME,
                            ft.Colors.DEEP_ORANGE,
                        ][i],
                        border_radius=10,
                        alignment=ft.Alignment.CENTER,
                    )
                    for i in range(12)
                ],
                runs_count=4,  # 每行显示的项数
                max_extent=150,  # 每项最大宽度
                child_aspect_ratio=1.0,  # 宽高比
                spacing=10,
                run_spacing=10,
                height=250,
            ),
        ])
    
    # ===== 页面布局 =====
    # 将所有内容放入一个支持水平和垂直滚动的布局中
    main_content = ft.Column(
        [
            ft.Text(
                "Flet 布局与自适应示例",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            ft.Divider(),
            
            create_layout_section(),
            ft.Divider(),
            create_expand_section(),
            ft.Divider(),
            create_stack_section(),
            ft.Divider(),
            create_responsive_section(),
            ft.Divider(),
            create_scroll_section(),
            ft.Divider(),
            create_grid_section(),
        ],
        spacing=20,
    )
    
    # 使用 Container 包装内容，设置最小宽度以触发水平滚动
    scrollable_content = ft.Container(
        content=main_content,
        padding=20,
        # 不设置固定宽度，让内容自适应
    )
    
    # 主布局：ListView 提供垂直滚动，Column 内的内容超出时页面水平滚动
    page.add(
        ft.Column(
            [scrollable_content],
            expand=True,
            scroll=ft.ScrollMode.AUTO,  # 垂直滚动
        )
    )
    
    # 启用页面级别的水平滚动
    page.scroll = ft.ScrollMode.AUTO


if __name__ == "__main__":
    ft.run(main)
