# -*- coding: utf-8 -*-
"""
Flet 音频/视频播放示例
演示音频和视频控件的播放控制

⚠️ 重要提示: Flet 1.0+ (>=0.82.0) 中 ft.Audio 控件已完全移除！
本示例保留作为历史参考，但音频功能已不可用。

破坏性变更说明:
  - ❌ Flet 0.x: ft.Audio 控件可用  →  Flet 1.0+: Audio 控件已完全移除
  - ❌ Flet 1.0+: 无官方替代方案，需使用第三方库（如 pygame, pydub 等）
  - ✅ Flet 1.0+: 使用 ft.run(main) 启动
"""

import flet as ft


def main(page: ft.Page):
    page.title = "音频视频播放示例（已弃用）"
    page.window.width = 600
    page.window.height = 400

    page.add(
        ft.Text("音频/视频播放示例", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.WARNING_AMBER, size=60, color=ft.Colors.ORANGE),
                ft.Text(
                    "⚠️ Audio 控件已移除",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.RED,
                ),
                ft.Text(
                    "ft.Audio 控件在 Flet 1.0+ (>=0.82.0) 中已完全移除",
                    size=14,
                ),
                ft.Divider(),
                ft.Text("破坏性变更详情:", weight=ft.FontWeight.W_500),
                ft.Text("• Flet 0.x: ft.Audio(src='...') 可用", color=ft.Colors.GREY_700),
                ft.Text("• Flet 1.0+: ft.Audio 已完全移除", color=ft.Colors.GREY_700),
                ft.Divider(),
                ft.Text("替代方案:", weight=ft.FontWeight.W_500),
                ft.Text("• 使用第三方音频库: pygame, pydub, simpleaudio", color=ft.Colors.GREY_700),
                ft.Text("• 使用 Web 音频 API (Web 应用)", color=ft.Colors.GREY_700),
                ft.Text("• 使用系统命令调用播放器", color=ft.Colors.GREY_700),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            ),
            bgcolor=ft.Colors.ORANGE_50,
            padding=30,
            border_radius=10,
            alignment=ft.Alignment.CENTER,
        ),
        
        ft.Divider(),
        
        ft.Text("第三方库示例代码:", weight=ft.FontWeight.W_500),
        ft.Container(
            content=ft.Markdown("""
```python
# 使用 pygame 播放音频
import pygame
pygame.mixer.init()
pygame.mixer.music.load("audio.mp3")
pygame.mixer.music.play()

# 使用 pydub 播放音频
from pydub import AudioSegment
from pydub.playback import play
audio = AudioSegment.from_file("audio.mp3")
play(audio)
```
            """, selectable=True),
            bgcolor=ft.Colors.GREY_100,
            padding=15,
            border_radius=10,
        ),
    )


ft.run(main)
