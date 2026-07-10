# Flet 1.0+ 示例代码索引

> 本目录包含 20 个完整示例，覆盖 Flet 1.0+ 的核心功能和常见场景。
> 
> **所有示例都经过验证，可直接运行。**

---

## 📋 示例列表

### 基础示例

| 文件 | 说明 | 关键知识点 |
|------|------|-----------|
| `01_basic_app.py` | 基础应用结构 | `ft.run()`、Page、Controls |
| `02_async_clock.py` | 异步时钟 | `asyncio`、`async def`、定时更新 |
| `03_form_validation.py` | 表单验证 | TextField、表单验证、错误提示 |

### 文件与服务

| 文件 | 说明 | 关键知识点 |
|------|------|-----------|
| `04_file_picker_service.py` | 文件选择器 | FilePicker、`page.services`、async API |
| `05_shared_preferences.py` | 本地存储 | SharedPreferences、数据持久化 |

### 动画与交互

| 文件 | 说明 | 关键知识点 |
|------|------|-----------|
| `06_animation_effects.py` | 动画效果 | `animate`、`animate_opacity`、`animate_rotation` |
| `13_drag_drop.py` | 拖拽功能 | Draggable、DragTarget |
| `14_keyboard_events.py` | 键盘事件 | `on_keyboard_event`、KeyboardEvent |
| `15_gestures.py` | 手势识别 | onTap、onLongPress、onScale |

### 布局与导航

| 文件 | 说明 | 关键知识点 |
|------|------|-----------|
| `08_layout_responsive.py` | 响应式布局 | ResponsiveRow、屏幕适配 |
| `09_theme_styling.py` | Tabs 三件套模式 | `Tabs` + `TabBar` + `TabBarView` |
| `10_navigation_menu.py` | 导航菜单 | NavigationRail、页面切换 |

### 对话框与提示

| 文件 | 说明 | 关键知识点 |
|------|------|-----------|
| `07_dialog_example.py` | 对话框 | `page.show_dialog()`、`page.pop_dialog()` |

### 数据与表格

| 文件 | 说明 | 关键知识点 |
|------|------|-----------|
| `11_data_table.py` | 数据表格 | DataTable、分页、排序 |

### 窗口控制

| 文件 | 说明 | 关键知识点 |
|------|------|-----------|
| `12_window_controls.py` | 窗口控制 | 窗口大小、位置、最小化 |

### 剪贴板与媒体

| 文件 | 说明 | 关键知识点 |
|------|------|-----------|
| `16_clipboard.py` | 剪贴板 | 复制、粘贴 |
| `17_media_player.py` | 媒体播放 | Video、Audio |

### 高级绘图

| 文件 | 说明 | 关键知识点 |
|------|------|-----------|
| `18_canvas_custom_paint.py` | Canvas 绘图 | CustomPainter、Canvas API |
| `19_file_operations.py` | 文件操作 | 读写文件、JSON 处理 |
| `20_charts_canvas_visualization.py` | 图表可视化 | Canvas 绘制图表 |

---

## 🚀 快速开始

### 运行示例

```bash
# 进入示例目录
cd examples

# 运行任意示例
flet run 01_basic_app.py
```

### 学习建议

1. **新手入门**：01 → 02 → 03 → 14（基础 + 键盘）
2. **布局学习**：08 → 09 → 10（响应式 + Tabs + 导航）
3. **动画学习**：06 → 13 → 15（动画 + 拖拽 + 手势）
4. **数据应用**：11 → 19 → 20（表格 + 文件 + 图表）

---

## ⚠️ 常见陷阱（必读）

### 键盘事件
```python
# ✅ 正确
def on_keyboard(e: ft.KeyboardEvent):
    if e.key == "Arrow Up":
        # 处理按键

# ❌ 错误 - KeyboardEvent 没有 event_type 属性
if e.event_type == "keydown":  # AttributeError!
```

### 对话框
```python
# ✅ 正确
page.show_dialog(dialog)
page.pop_dialog()

# ❌ 错误 - page.open() 不存在
page.open(dialog)  # AttributeError!
```

### Tabs（三件套模式）
```python
# ✅ 正确（Flet 1.0+）
ft.Tabs(
    content=ft.Column([
        ft.TabBar(tabs=[ft.Tab(label="标签1"), ft.Tab(label="标签2")]),
        ft.TabBarView(controls=[ft.Container(content=ft.Text("内容1")), ft.Container(content=ft.Text("内容2"))]),
    ]),
    length=2,
)

# ❌ 错误 - tabs 参数已移除
ft.Tabs(tabs=[ft.Tab(text="标签", content=...)])  # TypeError!
```

---

## 📚 参考文档

- [API Quick Reference](../references/api-quick-reference.md) - 高频 API 用法
- [Breaking Changes Guide](../references/breaking-changes.md) - 破坏性变更列表
- [Error Troubleshooting Guide](../references/error-guide.md) - 错误排查指南

---

**版本**: Flet >= 0.82.0  
**最后更新**: 2026-03-20
