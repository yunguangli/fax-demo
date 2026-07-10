# -*- coding: utf-8 -*-
"""
Flet 本地存储示例 - SharedPreferences
演示 Flet 1.0+ 中使用 shared_preferences 进行数据持久化

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: page.client_storage  →  Flet 1.0+: 已移除
  - ❌ Flet 0.x: page.shared_preferences  →  Flet 1.0+: 已移除
  - ✅ Flet 1.0+: 使用 ft.SharedPreferences() 类，先 page.services.append(prefs) 再使用
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动
"""

import flet as ft
import asyncio


def main(page: ft.Page):
    """SharedPreferences 示例主函数"""
    page.title = "本地存储示例"
    page.window.width = 600
    page.window.height = 500
    page.padding = 30
    
    # ✅ 创建 SharedPreferences 实例（Flet 1.0+ 新方式）
    prefs = ft.SharedPreferences()
    page.services.append(prefs)
    
    # 状态显示
    status_text = ft.Text(
        value="准备就绪",
        size=14,
        color=ft.Colors.GREY_600,
    )
    
    # 输入控件
    key_field = ft.TextField(
        label="键名 (Key)",
        hint_text="输入存储键名",
        width=250,
    )
    
    value_field = ft.TextField(
        label="值 (Value)",
        hint_text="输入存储值",
        width=250,
    )
    
    # 数据类型选择
    data_type = ft.Dropdown(
        label="数据类型",
        width=150,
        value="string",
        options=[
            ft.DropdownOption(key="string", text="字符串"),
            ft.DropdownOption(key="int", text="整数"),
            ft.DropdownOption(key="float", text="浮点数"),
            ft.DropdownOption(key="bool", text="布尔值"),
            ft.DropdownOption(key="list", text="列表(v0.82.2+)"),
        ],
    )
    
    # 存储的数据列表
    stored_data = ft.Column(scroll=ft.ScrollMode.AUTO, height=150)
    
    async def refresh_data_list():
        """刷新已存储数据列表"""
        try:
            # ✅ get_keys() 需要 key_prefix 参数，空字符串表示获取所有键
            keys = await prefs.get_keys("")
            
            stored_data.controls.clear()
            
            if not keys:
                stored_data.controls.append(
                    ft.Text("暂无存储的数据", color=ft.Colors.GREY_500, italic=True)
                )
            else:
                for key in keys:
                    value = await prefs.get(key)
                    stored_data.controls.append(
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.STORAGE, size=16, color=ft.Colors.BLUE),
                                ft.Text(f"{key}:", weight=ft.FontWeight.BOLD, width=100),
                                ft.Text(str(value), expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_size=18,
                                    tooltip="删除",
                                    on_click=lambda e, k=key: asyncio.create_task(delete_key(k)),
                                ),
                            ],
                            spacing=10,
                        )
                    )
            
            page.update()
        except Exception as ex:
            status_text.value = f"刷新列表失败: {str(ex)}"
            status_text.color = ft.Colors.RED
            page.update()
    
    async def save_value(e):
        """保存值"""
        try:
            key = key_field.value.strip()
            value = value_field.value
            
            if not key:
                status_text.value = "请输入键名"
                status_text.color = ft.Colors.RED
                page.update()
                return
            
            if not value:
                status_text.value = "请输入值"
                status_text.color = ft.Colors.RED
                page.update()
                return
            
            # 根据类型转换并保存（添加输入验证）
            data_type_val = data_type.value
            
            try:
                if data_type_val == "string":
                    await prefs.set(key, value)
                elif data_type_val == "int":
                    await prefs.set(key, int(value))
                elif data_type_val == "float":
                    await prefs.set(key, float(value))
                elif data_type_val == "bool":
                    await prefs.set(key, value.lower() in ("true", "1", "yes"))
                elif data_type_val == "list":
                    # v0.82.2+ 支持字符串列表
                    # 输入格式：用逗号分隔，如 "a,b,c"
                    list_value = [item.strip() for item in value.split(",") if item.strip()]
                    await prefs.set(key, list_value)
                
                status_text.value = f"[OK] 已保存: {key}"
                status_text.color = ft.Colors.GREEN
                
                # 清空输入
                key_field.value = ""
                value_field.value = ""
                
                # 刷新列表
                await refresh_data_list()
                
            except ValueError as ve:
                status_text.value = f"类型转换失败: 请输入有效的{data_type_val}值"
                status_text.color = ft.Colors.RED
                page.update()
            
        except Exception as ex:
            status_text.value = f"保存失败: {str(ex)}"
            status_text.color = ft.Colors.RED
            page.update()
    
    async def get_value(e):
        """获取值"""
        try:
            key = key_field.value.strip()
            
            if not key:
                status_text.value = "请输入键名"
                status_text.color = ft.Colors.RED
                page.update()
                return
            
            value = await prefs.get(key)
            
            if value is not None:
                value_field.value = str(value)
                status_text.value = f"[OK] 已读取: {key} = {value}"
                status_text.color = ft.Colors.GREEN
            else:
                status_text.value = f"键 '{key}' 不存在"
                status_text.color = ft.Colors.ORANGE
            
            page.update()
            
        except Exception as ex:
            status_text.value = f"读取失败: {str(ex)}"
            status_text.color = ft.Colors.RED
            page.update()
    
    async def delete_key(key: str):
        """删除指定键"""
        try:
            await prefs.remove(key)
            status_text.value = f"[OK] 已删除: {key}"
            status_text.color = ft.Colors.GREEN
            await refresh_data_list()
        except Exception as ex:
            status_text.value = f"删除失败: {str(ex)}"
            status_text.color = ft.Colors.RED
            page.update()
    
    async def clear_all(e):
        """清除所有数据"""
        try:
            await prefs.clear()
            status_text.value = "[OK] 已清除所有数据"
            status_text.color = ft.Colors.GREEN
            await refresh_data_list()
        except Exception as ex:
            status_text.value = f"清除失败: {str(ex)}"
            status_text.color = ft.Colors.RED
            page.update()
    
    # 页面布局
    page.add(
        ft.Column(
            [
                ft.Text(
                    "SharedPreferences 本地存储",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "数据持久化存储示例",
                    size=14,
                    color=ft.Colors.GREY_600,
                ),
                ft.Divider(),
                
                # 输入区域
                ft.Row(
                    [key_field, value_field, data_type],
                    spacing=10,
                ),
                
                # 按钮区域
                ft.Row(
                    [
                        ft.Button(
                            content=ft.Row(
                                [ft.Icon(ft.Icons.SAVE), ft.Text("保存")],
                                spacing=8,
                            ),
                            on_click=lambda e: asyncio.create_task(save_value(e)),
                        ),
                        ft.Button(
                            content=ft.Row(
                                [ft.Icon(ft.Icons.READ_MORE), ft.Text("读取")],
                                spacing=8,
                            ),
                            style=ft.ButtonStyle(
                                color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.GREEN,
                            ),
                            on_click=lambda e: asyncio.create_task(get_value(e)),
                        ),
                        ft.Button(
                            content=ft.Row(
                                [ft.Icon(ft.Icons.REFRESH), ft.Text("刷新列表")],
                                spacing=8,
                            ),
                            style=ft.ButtonStyle(
                                color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.BLUE,
                            ),
                            on_click=lambda e: asyncio.create_task(refresh_data_list()),
                        ),
                        ft.Button(
                            content=ft.Row(
                                [ft.Icon(ft.Icons.DELETE_FOREVER), ft.Text("清除全部")],
                                spacing=8,
                            ),
                            style=ft.ButtonStyle(
                                color=ft.Colors.RED,
                            ),
                            on_click=lambda e: asyncio.create_task(clear_all(e)),
                        ),
                    ],
                    wrap=True,
                    spacing=10,
                ),
                
                ft.Divider(),
                status_text,
                ft.Divider(),
                
                ft.Text("已存储的数据：", weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=stored_data,
                    border=ft.Border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    padding=10,
                    bgcolor=ft.Colors.GREY_50,
                ),
            ],
            spacing=15,
        )
    )
    
    # 初始化时刷新列表
    asyncio.create_task(refresh_data_list())


if __name__ == "__main__":
    ft.run(main)
