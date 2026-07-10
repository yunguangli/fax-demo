# -*- coding: utf-8 -*-
"""
Flet 主题配色示例
演示 Theme、ColorScheme、深色模式等主题设置

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: page.theme = ft.Theme(primary_swatch=...)  →  Flet 1.0+: 已移除
  - ✅ Flet 1.0+: 使用 page.theme = ft.Theme(color_scheme_seed=ft.Colors.XXX)
  - ❌ Flet 0.x: ft.Radio(value="1", label="...") 单独使用  →  Flet 1.0+: 报错 "Radio must be enclosed within RadioGroup"
  - ✅ Flet 1.0+: 必须用 ft.RadioGroup(content=ft.Radio(...)) 包裹
  - ❌ Flet 0.x: TabBarView 未设 height  →  Flet 1.0+: 报错 "height is unbounded"
  - ✅ Flet 1.0+: TabBarView 须直接设置 height=固定值（如 height=120）
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动
"""

import flet as ft


def main(page: ft.Page):
    """主题配色示例主函数"""
    page.title = "主题配色示例"
    page.window.width = 800
    page.window.height = 700
    page.padding = 20
    
    # ===== 主题状态 =====
    is_dark_mode = [False]
    current_theme_seed = [ft.Colors.BLUE]
    
    # ===== 颜色种子选项 =====
    theme_colors = [
        ("蓝色", ft.Colors.BLUE),
        ("红色", ft.Colors.RED),
        ("绿色", ft.Colors.GREEN),
        ("紫色", ft.Colors.PURPLE),
        ("橙色", ft.Colors.ORANGE),
        ("青色", ft.Colors.TEAL),
        ("粉色", ft.Colors.PINK),
        ("靛蓝", ft.Colors.INDIGO),
    ]
    
    def apply_theme():
        """应用主题"""
        # ✅ 使用 color_scheme_seed 替代已移除的 primary_swatch
        page.theme = ft.Theme(
            color_scheme_seed=current_theme_seed[0],
            use_material3=True,  # 使用 Material 3 设计
        )
        
        page.dark_theme = ft.Theme(
            color_scheme_seed=current_theme_seed[0],
            use_material3=True,
        )
        
        page.theme_mode = ft.ThemeMode.DARK if is_dark_mode[0] else ft.ThemeMode.LIGHT
        page.update()
    
    def toggle_theme(e):
        """切换深色/浅色模式"""
        is_dark_mode[0] = not is_dark_mode[0]
        theme_toggle.selected = is_dark_mode[0]
        apply_theme()
    
    def change_theme_color(e):
        """更改主题颜色"""
        current_theme_seed[0] = e.control.data
        apply_theme()
    
    # ===== 主题切换控件 =====
    theme_toggle = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        selected_icon=ft.Icons.DARK_MODE,
        selected=False,
        on_click=toggle_theme,
        tooltip="切换深色/浅色模式",
    )
    
    # ===== 颜色选择器 =====
    def create_color_buttons():
        """创建颜色选择按钮"""
        buttons = []
        for name, color in theme_colors:
            buttons.append(
                ft.IconButton(
                    icon=ft.Icons.PALETTE,
                    icon_color=color,
                    data=color,
                    on_click=change_theme_color,
                    tooltip=name,
                )
            )
        return buttons
    
    # ===== 示例组件展示 =====
    def create_sample_controls():
        """创建示例控件展示主题效果"""
        return ft.Column([
            ft.Text("主题效果预览", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            # 按钮
            ft.Row([
                ft.Button(content=ft.Text("主要按钮"), style=ft.ButtonStyle()),
                ft.Button(
                    content=ft.Text("自定义按钮"),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.RED,
                    ),
                ),
                ft.Button(
                    content=ft.Text("边框按钮"),
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(2, ft.Colors.BLUE),
                        color=ft.Colors.BLUE,
                    ),
                ),
            ], spacing=10),
            
            ft.Container(height=10),
            
            # 输入框
            ft.TextField(
                label="输入框",
                hint_text="请输入内容",
                width=300,
            ),
            
            ft.Container(height=10),
            
            # 卡片
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ALBUM),
                            title=ft.Text("卡片标题"),
                            subtitle=ft.Text("这是卡片的副标题说明"),
                        ),
                        ft.Row([
                            ft.Button(content=ft.Text("操作")),
                            ft.Button(content=ft.Text("取消")),
                        ], alignment=ft.MainAxisAlignment.END, spacing=10),
                    ]),
                    padding=10,
                ),
                elevation=4,
            ),
            
            ft.Container(height=10),
            
            # 进度条
            ft.Column([
                ft.Text("进度指示器:"),
                ft.ProgressBar(width=300, value=0.7),
                ft.Container(height=5),
                ft.ProgressRing(width=40, height=40, value=0.5),
            ]),
            
            ft.Container(height=10),
            
            # 开关和复选框
            ft.Row([
                ft.Switch(label="开关"),
                ft.Checkbox(label="复选框", value=True),
                ft.RadioGroup(
                    value="1",
                    content=ft.Radio(value="1", label="单选"),
                ),
            ], spacing=20),
            
            ft.Container(height=10),
            
            # 下拉框
            ft.Dropdown(
                label="下拉选择",
                width=200,
                options=[
                    ft.DropdownOption(key="1", text="选项 1"),
                    ft.DropdownOption(key="2", text="选项 2"),
                    ft.DropdownOption(key="3", text="选项 3"),
                ],
            ),
            
            ft.Container(height=10),
            
            # 滑块
            ft.Slider(
                label="滑块: {value}",
                min=0,
                max=100,
                value=50,
                width=300,
            ),
            
            ft.Container(height=10),
            
            # 选项卡（Flet 1.0+ 新 API：Tabs + TabBar + TabBarView）
            ft.Tabs(
                content=ft.Column([
                    ft.TabBar(
                        tabs=[
                            ft.Tab(
                                label=ft.Row([
                                    ft.Icon(ft.Icons.HOME, size=16),
                                    ft.Text("首页"),
                                ], spacing=5),
                            ),
                            ft.Tab(
                                label=ft.Row([
                                    ft.Icon(ft.Icons.SETTINGS, size=16),
                                    ft.Text("设置"),
                                ], spacing=5),
                            ),
                            ft.Tab(
                                label=ft.Row([
                                    ft.Icon(ft.Icons.INFO, size=16),
                                    ft.Text("关于"),
                                ], spacing=5),
                            ),
                        ],
                    ),
                    ft.TabBarView(
                        height=120,
                        controls=[
                            ft.Container(
                                content=ft.Text("这是首页的内容区域", color=ft.Colors.GREY_700),
                                padding=20,
                            ),
                            ft.Container(
                                content=ft.Text("这是设置的内容区域", color=ft.Colors.GREY_700),
                                padding=20,
                            ),
                            ft.Container(
                                content=ft.Text("这是关于的内容区域", color=ft.Colors.GREY_700),
                                padding=20,
                            ),
                        ],
                    ),
                ]),
                length=3,
                selected_index=0,
                width=400,
            ),
        ])
    
    # ===== ColorScheme 自定义 =====
    def create_color_scheme_section():
        """ColorScheme 自定义说明"""
        return ft.Column([
            ft.Text("ColorScheme 自定义", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.Text(
                "✅ 新版本推荐：使用 color_scheme_seed 自动生成配色方案",
                color=ft.Colors.GREEN,
            ),
            ft.Container(height=10),
            
            ft.Text("代码示例:"),
            ft.Container(
                content=ft.Column([
                    ft.Text("page.theme = ft.Theme(", font_family="monospace", size=12),
                    ft.Text("    color_scheme_seed=ft.Colors.BLUE,", font_family="monospace", size=12),
                    ft.Text("    use_material3=True,", font_family="monospace", size=12),
                    ft.Text(")", font_family="monospace", size=12),
                ]),
                bgcolor=ft.Colors.GREY_200 if not is_dark_mode[0] else ft.Colors.GREY_800,
                padding=15,
                border_radius=8,
            ),
            
            ft.Container(height=15),
            
            ft.Text("❌ 已移除的属性:", color=ft.Colors.RED),
            ft.Container(
                content=ft.Column([
                    ft.Text("primary_swatch → 使用 color_scheme_seed", font_family="monospace", size=12),
                    ft.Text("primary_color → 使用 ColorScheme.primary", font_family="monospace", size=12),
                    ft.Text("primary_color_dark → 已移除", font_family="monospace", size=12),
                    ft.Text("primary_color_light → 已移除", font_family="monospace", size=12),
                    ft.Text("shadow_color → 使用 ColorScheme.shadow", font_family="monospace", size=12),
                    ft.Text("divider_color → 使用 DividerTheme.color", font_family="monospace", size=12),
                ]),
                bgcolor=ft.Colors.RED_50 if not is_dark_mode[0] else ft.Colors.RED_900,
                padding=15,
                border_radius=8,
            ),
        ])
    
    # ===== 高级主题自定义 =====
    def create_advanced_theme_section():
        """高级主题自定义"""
        return ft.Column([
            ft.Text("高级主题自定义", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.Text("自定义控件主题:"),
            ft.Container(
                content=ft.Column([
                    ft.Text("# 按钮主题", weight=ft.FontWeight.BOLD),
                    ft.Text("page.theme.floating_action_button_theme =", font_family="monospace", size=11),
                    ft.Text("    ft.FloatingActionButtonTheme(bgcolor=ft.Colors.RED)", font_family="monospace", size=11),
                    ft.Text(""),
                    ft.Text("# 卡片主题", weight=ft.FontWeight.BOLD),
                    ft.Text("page.theme.card_theme =", font_family="monospace", size=11),
                    ft.Text("    ft.CardTheme(elevation=8, shape=ft.RoundedRectangleBorder(radius=10))", font_family="monospace", size=11),
                    ft.Text(""),
                    ft.Text("# 输入框主题", weight=ft.FontWeight.BOLD),
                    ft.Text("page.theme.input_decoration_theme =", font_family="monospace", size=11),
                    ft.Text("    ft.InputDecorationTheme(filled=True, fillColor=ft.Colors.GREY_100)", font_family="monospace", size=11),
                ]),
                bgcolor=ft.Colors.GREY_200 if not is_dark_mode[0] else ft.Colors.GREY_800,
                padding=15,
                border_radius=8,
            ),
            
            ft.Container(height=10),
            
            # 示例卡片
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.INFO, color=ft.Colors.BLUE),
                            title=ft.Text("主题继承说明"),
                            subtitle=ft.Text("子控件会自动继承父控件的主题设置"),
                        ),
                    ]),
                    padding=10,
                ),
            ),
        ])
    
    # ===== 页面布局 =====
    page.add(
        ft.Column([
            # 标题栏
            ft.Row([
                ft.Text(
                    "主题配色示例",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
                theme_toggle,
                *create_color_buttons(),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Divider(),
            
            # 内容区域
            ft.Row([
                ft.Column([
                    create_sample_controls(),
                ], scroll=ft.ScrollMode.AUTO, expand=True),
                
                ft.VerticalDivider(),
                
                ft.Column([
                    create_color_scheme_section(),
                    ft.Divider(),
                    create_advanced_theme_section(),
                ], scroll=ft.ScrollMode.AUTO, width=350),
            ], expand=True),
        ], expand=True)
    )
    
    # 初始化主题
    apply_theme()


if __name__ == "__main__":
    ft.run(main)
