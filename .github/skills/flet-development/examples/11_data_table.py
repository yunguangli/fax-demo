# -*- coding: utf-8 -*-
"""
Flet 数据表格示例
演示 DataTable、ListView、GridView 等数据展示控件

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: list_view.scroll_to(key="item_1")  →  Flet 1.0+: 参数名改为 scroll_key
  - ✅ Flet 1.0+: 使用 list_view.scroll_to(scroll_key="item_1")
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动
"""

import flet as ft


def main(page: ft.Page):
    """数据表格示例主函数"""
    page.title = "数据表格示例"
    page.window.width = 900
    page.window.height = 700
    page.padding = 20
    
    # ===== 1. DataTable 表格 =====
    def create_datatable_section():
        """数据表格"""
        return ft.Column([
            ft.Text("1. DataTable 数据表格", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("姓名", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("年龄", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("城市", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("操作", weight=ft.FontWeight.BOLD)),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("001")),
                            ft.DataCell(ft.Text("张三")),
                            ft.DataCell(ft.Text("25")),
                            ft.DataCell(ft.Text("北京")),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(icon=ft.Icons.EDIT, icon_size=18, tooltip="编辑"),
                                    ft.IconButton(icon=ft.Icons.DELETE, icon_size=18, tooltip="删除", icon_color=ft.Colors.RED),
                                ], spacing=0)
                            ),
                        ],
                    ),
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("002")),
                            ft.DataCell(ft.Text("李四")),
                            ft.DataCell(ft.Text("30")),
                            ft.DataCell(ft.Text("上海")),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(icon=ft.Icons.EDIT, icon_size=18, tooltip="编辑"),
                                    ft.IconButton(icon=ft.Icons.DELETE, icon_size=18, tooltip="删除", icon_color=ft.Colors.RED),
                                ], spacing=0)
                            ),
                        ],
                    ),
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("003")),
                            ft.DataCell(ft.Text("王五")),
                            ft.DataCell(ft.Text("28")),
                            ft.DataCell(ft.Text("广州")),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(icon=ft.Icons.EDIT, icon_size=18, tooltip="编辑"),
                                    ft.IconButton(icon=ft.Icons.DELETE, icon_size=18, tooltip="删除", icon_color=ft.Colors.RED),
                                ], spacing=0)
                            ),
                        ],
                    ),
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("004")),
                            ft.DataCell(ft.Text("赵六")),
                            ft.DataCell(ft.Text("35")),
                            ft.DataCell(ft.Text("深圳")),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(icon=ft.Icons.EDIT, icon_size=18, tooltip="编辑"),
                                    ft.IconButton(icon=ft.Icons.DELETE, icon_size=18, tooltip="删除", icon_color=ft.Colors.RED),
                                ], spacing=0)
                            ),
                        ],
                    ),
                ],
                border=ft.Border.all(1, ft.Colors.GREY_300),
                border_radius=10,
                vertical_lines=ft.BorderSide(1, ft.Colors.GREY_200),
                horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
                heading_row_color=ft.Colors.GREY_100,
                heading_row_height=50,
                data_row_min_height=45,
                data_row_max_height=60,
            ),
        ])
    
    # ===== 2. ListView 列表 =====
    list_view = ft.ListView(
        spacing=5,
        padding=10,
        item_extent=60,  # 固定项高度，提升性能
        height=250,
        width=400,
    )
    
    # 添加初始数据
    for i in range(50):
        list_view.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE),
                    ft.Text(f"用户 {i + 1}"),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_400, size=16),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=10,
                bgcolor=ft.Colors.GREY_50,
                border_radius=5,
                on_click=lambda e, idx=i: print(f"点击了用户 {idx + 1}"),
            )
        )
    
    def create_listview_section():
        """ListView 列表"""
        return ft.Column([
            ft.Text("2. ListView 列表（虚拟滚动）", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.Text("适用于长列表，支持虚拟滚动提升性能", color=ft.Colors.GREY_600, size=12),
            
            ft.Row([
                list_view,
                ft.Column([
                    ft.Button(
                        content=ft.Row([ft.Icon(ft.Icons.ARROW_UPWARD), ft.Text("滚动到顶部")]),
                        on_click=lambda e: scroll_to_top(),
                    ),
                    ft.Button(
                        content=ft.Row([ft.Icon(ft.Icons.ARROW_DOWNWARD), ft.Text("滚动到底部")]),
                        on_click=lambda e: scroll_to_bottom(),
                    ),
                ], spacing=10),
            ]),
        ])
    
    def scroll_to_top():
        """滚动到顶部"""
        # ✅ Flet 1.0+ 使用 scroll_key 参数
        list_view.scroll_to(offset=0, duration=500)
        page.update()
    
    def scroll_to_bottom():
        """滚动到底部"""
        list_view.scroll_to(offset=-1, duration=500)
        page.update()
    
    # ===== 3. GridView 网格 =====
    def create_gridview_section():
        """GridView 网格"""
        return ft.Column([
            ft.Text("3. GridView 网格视图", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.GridView(
                [
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.IMAGE, size=40, color=ft.Colors.GREY_400),
                            ft.Text(f"图片 {i + 1}", size=12),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                        bgcolor=ft.Colors.GREY_100,
                        border_radius=10,
                        alignment=ft.Alignment.CENTER,
                    )
                    for i in range(20)
                ],
                runs_count=4,
                max_extent=120,
                child_aspect_ratio=1.0,
                spacing=10,
                run_spacing=10,
                height=300,
                width=500,
            ),
        ])
    
    # ===== 4. ExpansionTile 可展开列表 =====
    def create_expansion_section():
        """可展开列表"""
        return ft.Column([
            ft.Text("4. ExpansionTile 可展开列表", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.Column([
                ft.ExpansionTile(
                    title=ft.Text("分组 1: 基本信息"),
                    subtitle=ft.Text("包含用户基本资料"),
                    leading=ft.Icon(ft.Icons.INFO),
                    trailing=ft.Icon(ft.Icons.EXPAND_MORE),
                    controls=[
                        ft.ListTile(title=ft.Text("姓名: 张三")),
                        ft.ListTile(title=ft.Text("年龄: 25")),
                        ft.ListTile(title=ft.Text("城市: 北京")),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("分组 2: 联系方式"),
                    subtitle=ft.Text("包含联系信息"),
                    leading=ft.Icon(ft.Icons.CONTACT_PHONE),
                    trailing=ft.Icon(ft.Icons.EXPAND_MORE),
                    controls=[
                        ft.ListTile(title=ft.Text("电话: 138****1234")),
                        ft.ListTile(title=ft.Text("邮箱: test@example.com")),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("分组 3: 设置"),
                    subtitle=ft.Text("应用设置选项"),
                    leading=ft.Icon(ft.Icons.SETTINGS),
                    trailing=ft.Icon(ft.Icons.EXPAND_MORE),
                    controls=[
                        ft.Switch(label="通知"),
                        ft.Switch(label="自动更新"),
                        ft.Switch(label="深色模式"),
                    ],
                ),
            ], spacing=5),
        ])
    
    # ===== 5. 分页示例 =====
    current_page = [1]
    items_per_page = 5
    total_items = 47
    
    def get_page_items(page_num: int) -> list:
        """获取指定页的数据"""
        start = (page_num - 1) * items_per_page
        end = start + items_per_page
        return [f"数据项 {i + 1}" for i in range(start, min(end, total_items))]
    
    page_list = ft.Column(spacing=5)
    
    def update_page_list():
        """更新页面列表"""
        page_list.controls.clear()
        for item in get_page_items(current_page[0]):
            page_list.controls.append(
                ft.Container(
                    content=ft.Text(item),
                    padding=10,
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=5,
                )
            )
        page_info.value = f"第 {current_page[0]} 页 / 共 {(total_items + items_per_page - 1) // items_per_page} 页"
        page.update()
    
    def prev_page(e):
        """上一页"""
        if current_page[0] > 1:
            current_page[0] -= 1
            update_page_list()
    
    def next_page(e):
        """下一页"""
        max_page = (total_items + items_per_page - 1) // items_per_page
        if current_page[0] < max_page:
            current_page[0] += 1
            update_page_list()
    
    page_info = ft.Text()
    
    def create_pagination_section():
        """分页示例"""
        return ft.Column([
            ft.Text("5. 分页示例", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.Container(
                content=page_list,
                height=200,
                width=300,
            ),
            
            ft.Row([
                ft.Button(
                    content=ft.Icon(ft.Icons.CHEVRON_LEFT),
                    on_click=prev_page,
                ),
                page_info,
                ft.Button(
                    content=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                    on_click=next_page,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ])
    
    # ===== 初始化分页 =====
    update_page_list()
    
    # ===== 页面布局 =====
    page.add(
        ft.Column([
            ft.Text(
                "数据表格示例",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            ft.Divider(),
            
            ft.Row([
                ft.Column([
                    create_datatable_section(),
                    ft.Divider(),
                    create_listview_section(),
                ], scroll=ft.ScrollMode.AUTO, expand=True),
                
                ft.VerticalDivider(),
                
                ft.Column([
                    create_gridview_section(),
                    ft.Divider(),
                    create_expansion_section(),
                    ft.Divider(),
                    create_pagination_section(),
                ], scroll=ft.ScrollMode.AUTO, expand=True),
            ], expand=True),
        ], expand=True)
    )


if __name__ == "__main__":
    ft.run(main)
