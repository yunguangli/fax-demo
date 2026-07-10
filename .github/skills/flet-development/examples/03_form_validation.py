# -*- coding: utf-8 -*-
"""
Flet 表单验证示例
演示表单输入、验证和提交

适用版本: Flet >= 0.82.0 (Flet 1.0+)

破坏性变更说明:
  - ❌ Flet 0.x: ft.app(target=main)  →  Flet 1.0+: 报错
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动
  - ✅ Flet 1.0+: 所有颜色使用 ft.Colors.XXX（大写 C）
"""

import flet as ft
import re


def main(page: ft.Page):
    """表单应用主函数"""
    page.title = "用户注册表单"
    page.window.width = 500
    page.window.height = 600
    page.padding = 30
    
    # 表单控件
    name_field = ft.TextField(
        label="姓名",
        hint_text="请输入您的姓名",
        width=400,
        prefix_icon=ft.Icons.PERSON,
    )
    
    email_field = ft.TextField(
        label="邮箱",
        hint_text="请输入有效的邮箱地址",
        width=400,
        prefix_icon=ft.Icons.EMAIL,
    )
    
    password_field = ft.TextField(
        label="密码",
        hint_text="至少8位，包含字母和数字",
        width=400,
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
    )
    
    confirm_password_field = ft.TextField(
        label="确认密码",
        hint_text="再次输入密码",
        width=400,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
    )
    
    # 错误提示
    error_text = ft.Text(
        color=ft.Colors.RED,
        size=14,
        weight=ft.FontWeight.W_500,
    )
    
    # 成功提示
    success_text = ft.Text(
        color=ft.Colors.GREEN,
        size=14,
        weight=ft.FontWeight.W_500,
    )
    
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(password: str) -> bool:
        """验证密码强度"""
        if len(password) < 8:
            return False
        has_letter = any(c.isalpha() for c in password)
        has_number = any(c.isdigit() for c in password)
        return has_letter and has_number
    
    def validate_and_submit(e):
        """验证表单并提交"""
        errors = []
        
        # 验证姓名
        if not name_field.value or not name_field.value.strip():
            errors.append("• 姓名不能为空")
        
        # 验证邮箱
        if not email_field.value:
            errors.append("• 邮箱不能为空")
        elif not validate_email(email_field.value):
            errors.append("• 请输入有效的邮箱地址")
        
        # 验证密码
        if not password_field.value:
            errors.append("• 密码不能为空")
        elif not validate_password(password_field.value):
            errors.append("• 密码至少8位，需包含字母和数字")
        
        # 验证确认密码
        if password_field.value != confirm_password_field.value:
            errors.append("• 两次输入的密码不一致")
        
        # 显示结果
        if errors:
            error_text.value = "\n".join(errors)
            success_text.value = ""
        else:
            error_text.value = ""
            success_text.value = "✓ 注册成功！"
            print(f"注册信息：{name_field.value}, {email_field.value}")
        
        page.update()
    
    def reset_form(e):
        """重置表单"""
        name_field.value = ""
        email_field.value = ""
        password_field.value = ""
        confirm_password_field.value = ""
        error_text.value = ""
        success_text.value = ""
        page.update()
    
    # 按钮
    submit_button = ft.Button(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CHECK, size=18),
                ft.Text("提交注册"),
            ],
            spacing=8,
        ),
        width=400,
        height=45,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE,
        ),
        on_click=validate_and_submit,
    )
    
    reset_button = ft.Button(
        content=ft.Text("重置"),
        width=400,
        height=45,
        on_click=reset_form,
    )
    
    # 组装表单
    page.add(
        ft.Column(
            [
                ft.Text(
                    "用户注册",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
                ft.Divider(),
                name_field,
                email_field,
                password_field,
                confirm_password_field,
                ft.Container(height=10),
                error_text,
                success_text,
                ft.Container(height=10),
                submit_button,
                reset_button,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.run(main)
