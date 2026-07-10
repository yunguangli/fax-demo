# -*- coding: utf-8 -*-
"""
Flet 导航菜单示例
演示 NavigationRail、NavigationDrawer、AppBar 等导航控件

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: ft.Tabs(tabs=[ft.Tab(text=..., content=...)])  →  Flet 1.0+: 报错 "unexpected keyword argument 'tabs'"
  - ❌ Flet 0.x: ft.Tab(content=...)  →  Flet 1.0+: 报错 "unexpected keyword argument 'content'"
  - ✅ Flet 1.0+: 使用 ft.Tabs(content=..., length=N) + ft.TabBar(tabs=[...]) + ft.TabBarView(controls=[...])
  - ✅ Flet 1.0+: TabBarView 须直接设置 height=固定值（如 height=120）
  - ❌ Flet 0.x: NavigationDrawer 有 position 属性  →  Flet 1.0+: 已移除
  - ✅ Flet 1.0+: 必须使用 page.drawer = drawer 设置（不能用 page.overlay.append）
  - ❌ Flet 0.x / 错误用法: page.drawer.open = True  →  Flet 1.0+: 'NavigationDrawer' object has no attribute 'open'
  - ✅ Flet 1.0+: 使用 await page.show_drawer() / await page.close_drawer() 控制开关
  - ✅ Flet 1.0+: 右侧抽屉使用 page.end_drawer
  - ❌ Flet 0.x: ft.PopupMenuItem(text="...")  →  Flet 1.0+: 报错 "unexpected keyword argument 'text'"
  - ✅ Flet 1.0+: 使用 ft.PopupMenuItem(content=ft.Text("..."))

功能说明:
  - 点击左上角菜单按钮：折叠/展开左侧 NavigationRail 侧边栏
  - NavigationRail.extended 属性控制是否显示标签文字
"""

import flet as ft
import asyncio


def main(page: ft.Page):
    """导航菜单示例主函数"""
    page.title = "导航菜单示例"
    page.window.width = 900
    page.window.height = 650
    
    # 当前选中的页面索引
    selected_index = [0]
    
    # ===== 页面内容 =====
    def get_page_content(index: int) -> ft.Control:
        """根据索引获取页面内容"""
        contents = [
            # 首页
            ft.Column([
                ft.Icon(ft.Icons.HOME, size=60, color=ft.Colors.BLUE),
                ft.Text("首页", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("欢迎来到应用首页", color=ft.Colors.GREY_600),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            
            # 搜索
            ft.Column([
                ft.Icon(ft.Icons.SEARCH, size=60, color=ft.Colors.GREEN),
                ft.Text("搜索", size=24, weight=ft.FontWeight.BOLD),
                ft.TextField(
                    label="搜索内容",
                    hint_text="输入搜索关键词",
                    width=300,
                    prefix_icon=ft.Icons.SEARCH,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            
            # 收藏
            ft.Column([
                ft.Icon(ft.Icons.FAVORITE, size=60, color=ft.Colors.RED),
                ft.Text("收藏", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("您收藏的内容将显示在这里", color=ft.Colors.GREY_600),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            
            # 设置
            ft.Column([
                ft.Icon(ft.Icons.SETTINGS, size=60, color=ft.Colors.PURPLE),
                ft.Text("设置", size=24, weight=ft.FontWeight.BOLD),
                ft.Switch(label="深色模式"),
                ft.Switch(label="通知"),
                ft.Switch(label="自动更新"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
        ]
        return contents[index] if index < len(contents) else contents[0]
    
    # ===== AppBar 顶部导航栏 =====
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            tooltip="折叠/展开侧边栏",
            on_click=lambda e: toggle_rail(),  # ✅ 切换 NavigationRail 折叠/展开
        ),
        leading_width=40,
        title=ft.Text("导航菜单示例", weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        actions=[
            ft.IconButton(icon=ft.Icons.SEARCH, tooltip="搜索"),
            ft.IconButton(icon=ft.Icons.NOTIFICATIONS, tooltip="通知"),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(content=ft.Text("个人资料")),  # ✅ Flet 1.0+: 使用 content，不能用 text
                    ft.PopupMenuItem(content=ft.Text("账户设置")),
                    ft.PopupMenuItem(),  # 分隔符
                    ft.PopupMenuItem(content=ft.Text("退出登录")),
                ],
                icon=ft.Icons.MORE_VERT,
            ),
        ],
    )
    
    # ===== NavigationDrawer 侧边抽屉 =====
    # ✅ Flet 1.0+: NavigationDrawer 必须通过 page.drawer 设置（不是 overlay）
    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=60, color=ft.Colors.BLUE),
                    ft.Text("用户名", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("user@example.com", color=ft.Colors.GREY_600, size=12),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                bgcolor=ft.Colors.BLUE_50,
            ),
            ft.Divider(),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="首页",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.SEARCH_OUTLINED,
                selected_icon=ft.Icons.SEARCH,
                label="搜索",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.FAVORITE_BORDER,
                selected_icon=ft.Icons.FAVORITE,
                label="收藏",
            ),
            ft.Divider(),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="设置",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.HELP_OUTLINE,
                selected_icon=ft.Icons.HELP,
                label="帮助",
            ),
        ],
        on_change=lambda e: on_drawer_change(e),
    )
    
    # 设置到 page.drawer（必须通过 page.drawer 才能控制 open 属性）
    page.drawer = drawer
    
    def toggle_rail():
        """切换 NavigationRail 折叠/展开"""
        # ✅ 切换 extended 属性实现折叠/展开
        rail.extended = not rail.extended
        rail.update()
    
    async def on_drawer_change(e):
        """抽屉导航变更"""
        selected_index[0] = e.control.selected_index
        content_container.content = get_page_content(selected_index[0])
        await page.close_drawer()  # ✅ Flet 1.0+: 使用 await page.close_drawer()
    
    # ===== NavigationRail 侧边导航栏 =====
    # ✅ 支持 extended 属性控制折叠/展开
    rail = ft.NavigationRail(
        selected_index=0,
        extended=True,  # 初始展开状态
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=56,
        min_extended_width=150,
        leading=ft.FloatingActionButton(
            content=ft.Icon(ft.Icons.ADD),
            on_click=lambda e: print("添加按钮点击"),
        ),
        trailing=ft.IconButton(
            icon=ft.Icons.SETTINGS_OUTLINED,
            on_click=lambda e: print("设置点击"),
        ),
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="首页",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SEARCH_OUTLINED,
                selected_icon=ft.Icons.SEARCH,
                label="搜索",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FAVORITE_BORDER,
                selected_icon=ft.Icons.FAVORITE,
                label="收藏",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="设置",
            ),
        ],
        on_change=lambda e: on_rail_change(e),
    )
    
    def on_rail_change(e):
        """Rail 导航变更"""
        selected_index[0] = e.control.selected_index
        content_container.content = get_page_content(selected_index[0])
        page.update()
    
    # ===== 底部导航栏 =====
    bottom_nav = ft.NavigationBar(
        selected_index=0,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="首页",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SEARCH_OUTLINED,
                selected_icon=ft.Icons.SEARCH,
                label="搜索",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.FAVORITE_BORDER,
                selected_icon=ft.Icons.FAVORITE,
                label="收藏",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="设置",
            ),
        ],
        on_change=lambda e: on_bottom_nav_change(e),
    )
    
    def on_bottom_nav_change(e):
        """底部导航变更"""
        selected_index[0] = e.control.selected_index
        content_container.content = get_page_content(selected_index[0])
        rail.selected_index = selected_index[0]
        page.update()
    
    # ===== 内容区域 =====
    content_container = ft.Container(
        content=get_page_content(0),
        expand=True,
        alignment=ft.Alignment.CENTER,
    )
    
    # ===== Tabs 导航 =====
    def create_tabs_section():
        """Tabs 标签导航（Flet 1.0+ 新 API）"""
        return ft.Column([
            ft.Text("Tabs 标签导航", size=16, weight=ft.FontWeight.BOLD),
            ft.Tabs(
                content=ft.Column([
                    ft.TabBar(
                        tabs=[
                            ft.Tab(
                                label=ft.Row([
                                    ft.Icon(ft.Icons.INFO, size=16),
                                    ft.Text("信息"),
                                ], spacing=5),
                            ),
                            ft.Tab(
                                label=ft.Row([
                                    ft.Icon(ft.Icons.LIST, size=16),
                                    ft.Text("列表"),
                                ], spacing=5),
                            ),
                            ft.Tab(
                                label=ft.Row([
                                    ft.Icon(ft.Icons.SETTINGS, size=16),
                                    ft.Text("设置"),
                                ], spacing=5),
                            ),
                        ],
                    ),
                    ft.TabBarView(
                        height=120,  # ✅ Flet 1.0+: 必须设置固定高度
                        controls=[
                            ft.Container(
                                content=ft.Text("信息标签页内容", color=ft.Colors.GREY_700),
                                padding=20,
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("列表项 1"),
                                    ft.Text("列表项 2"),
                                    ft.Text("列表项 3"),
                                ]),
                                padding=20,
                            ),
                            ft.Container(
                                content=ft.Text("设置标签页内容", color=ft.Colors.GREY_700),
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
    
    # ===== 使用说明 =====
    def create_info_section():
        """使用说明"""
        return ft.Container(
            content=ft.Column([
                ft.Text("导航控件使用说明", size=16, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Markdown("""
**AppBar** - 顶部导航栏
- 使用 `page.appbar` 属性设置
- 支持标题、图标按钮、菜单等

**NavigationRail** - 侧边导航栏
- 适用于桌面端侧边导航
- 支持折叠/展开模式

**NavigationBar** - 底部导航栏
- 适用于移动端底部导航
- 最多 5 个目标

**NavigationDrawer** - 侧边抽屉
- ✅ **Flet 1.0+ 变更**: 使用 `page.overlay.append(drawer)` 替代 `page.drawer`
- 支持左侧或右侧抽屉

**Tabs** - 标签页导航
- ✅ **Flet 1.0+ 变更**: 使用 `label` 替代 `text` 和 `tab_content`
                """, selectable=True),
            ]),
            bgcolor=ft.Colors.BLUE_50,
            padding=15,
            border_radius=10,
            width=400,
        )
    
    # ===== 主布局 =====
    page.add(
        ft.Row([
            rail,
            ft.VerticalDivider(width=1),
            ft.Column([
                content_container,
                ft.Divider(),
                ft.Row([
                    create_tabs_section(),
                    create_info_section(),
                ], spacing=20),
            ], expand=True, scroll=ft.ScrollMode.AUTO),
        ], expand=True)
    )
    
    # 设置底部导航（可选，注释掉以避免与 rail 冲突）
    # page.bottom_navigation_bar = bottom_nav


if __name__ == "__main__":
    ft.run(main)
