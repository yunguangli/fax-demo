# Flet 1.0+ 新增控件详解

> 本文档介绍 Flet 1.0+ (>=0.82.0) 新增的 19 个控件，包括 Material Design 3 按钮系列、输入控件、列表控件、菜单控件、效果和工具控件。

---

## Material Design 3 按钮系列

### FilledIconButton - 填充图标按钮

用于主要操作的图标按钮，使用填充背景色。

```python
import flet as ft

# 基本用法
ft.FilledIconButton(icon=ft.Icons.CHECK)

# 带样式的填充图标按钮
ft.FilledIconButton(
    icon=ft.Icons.SAVE,
    tooltip="保存文件",
    on_click=handle_save,
)
```

---

### FilledTonalButton - 填充色调按钮

介于 FilledButton 和 OutlinedButton 之间的按钮样式，使用次要颜色填充背景。

```python
import flet as ft

# 基本用法
ft.FilledTonalButton(content=ft.Text("Filled tonal button"))

# 带图标的填充色调按钮
ft.FilledTonalButton(
    content=ft.Text("添加项目"),
    icon=ft.Icons.ADD_OUTLINED,
    on_click=handle_add,
)

# 完整示例
ft.FilledTonalButton(
    content=ft.Text("设置"),
    icon=ft.Icons.SETTINGS_OUTLINED,
    style=ft.ButtonStyle(
        padding=ft.Padding(horizontal=20, vertical=12),
    ),
)
```

---

### FilledTonalIconButton - 填充色调图标按钮

使用次要颜色填充背景的图标按钮。

```python
import flet as ft

# 基本用法
ft.FilledTonalIconButton(icon=ft.Icons.SETTINGS)

# 带提示的填充色调图标按钮
ft.FilledTonalIconButton(
    icon=ft.Icons.FAVORITE,
    tooltip="收藏",
    selected_icon=ft.Icons.FAVORITE_BORDER,
    on_click=toggle_favorite,
)
```

---

### OutlinedIconButton - 边框图标按钮

带边框的图标按钮，用于次要操作。

```python
import flet as ft

# 基本用法
ft.OutlinedIconButton(icon=ft.Icons.SEARCH)

# 带样式的边框图标按钮
ft.OutlinedIconButton(
    icon=ft.Icons.DELETE_OUTLINE,
    tooltip="删除",
    style=ft.ButtonStyle(
        side=ft.BorderSide(2, ft.Colors.RED),
    ),
    on_click=handle_delete,
)
```

---

## 输入控件

### SearchBar - 搜索栏

带有搜索建议的输入控件，支持实时搜索和视图展开。

```python
import flet as ft

def main(page: ft.Page):
    def handle_change(e):
        print(f"搜索内容: {e.data}")
        # 根据输入更新建议列表
        
    def handle_submit(e):
        print(f"提交搜索: {e.data}")
        
    def handle_tap(e):
        print("搜索栏被点击")
    
    search_bar = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.Colors.AMBER,
        bar_hint_text="搜索颜色...",
        view_hint_text="从建议中选择颜色...",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=[
            ft.ListTile(
                title=ft.Text("红色"),
                on_click=lambda e: print("选择红色"),
            ),
            ft.ListTile(
                title=ft.Text("蓝色"),
                on_click=lambda e: print("选择蓝色"),
            ),
            ft.ListTile(
                title=ft.Text("绿色"),
                on_click=lambda e: print("选择绿色"),
            ),
        ],
    )
    
    page.add(search_bar)

ft.run(main)
```

**属性说明：**
- `view_elevation`：建议列表的阴影高度
- `divider_color`：分隔线颜色
- `bar_hint_text`：搜索栏占位文本
- `view_hint_text`：建议视图提示文本
- `on_change`：输入内容变化时触发
- `on_submit`：提交搜索时触发
- `on_tap`：点击搜索栏时触发
- `controls`：建议列表项

---

### AutoComplete - 自动完成

带有自动建议功能的输入控件。

```python
import flet as ft

def main(page: ft.Page):
    numbers = [
        ("one", "One"),
        ("two", "Two"),
        ("three", "Three"),
        ("four", "Four"),
        ("five", "Five"),
    ]
    
    def handle_change(e):
        print(f"输入变化: {e.control.value}")
        
    def handle_select(e):
        print(f"选中: {e.selection.key} = {e.selection.value}")
    
    autocomplete = ft.AutoComplete(
        value="One",
        width=200,
        on_change=handle_change,
        on_select=handle_select,
        suggestions=[
            ft.AutoCompleteSuggestion(key=key, value=value)
            for key, value in numbers
        ],
    )
    
    page.add(autocomplete)

ft.run(main)
```

**属性说明：**
- `value`：初始值
- `suggestions`：建议列表，使用 `AutoCompleteSuggestion` 对象
- `on_change`：输入变化时触发
- `on_select`：选择建议时触发

---

### DropdownM2 - Material Design 3 风格下拉菜单

Material Design 3 风格的下拉选择控件。

```python
import flet as ft
from flet import dropdownm2

def main(page: ft.Page):
    dropdown = ft.DropdownM2(
        width=220,
        value="Alice",
        label="选择用户",
        on_change=lambda e: print(f"选中: {e.control.value}"),
        options=[
            dropdownm2.Option(key="Alice", text="Alice"),
            dropdownm2.Option(key="Bob", text="Bob"),
            dropdownm2.Option(key="Charlie", text="Charlie"),
        ],
    )
    
    page.add(dropdown)

ft.run(main)
```

**属性说明：**
- `value`：选中的值
- `label`：标签文本
- `options`：选项列表，使用 `dropdownm2.Option`
- `on_change`：选择变化时触发

---

### RangeSlider - 范围滑块

支持选择区间的滑块控件。

```python
import flet as ft

def main(page: ft.Page):
    def handle_slider_change_start(e):
        print(f"开始拖动: {e.control.start_value} - {e.control.end_value}")
        
    def handle_slider_change(e):
        print(f"拖动中: {e.control.start_value} - {e.control.end_value}")
        
    def handle_slider_change_end(e):
        print(f"结束拖动: {e.control.start_value} - {e.control.end_value}")
    
    range_slider = ft.RangeSlider(
        min=0,
        max=100,
        start_value=10,
        end_value=20,
        divisions=10,
        label="{value}%",
        on_change_start=handle_slider_change_start,
        on_change=handle_slider_change,
        on_change_end=handle_slider_change_end,
    )
    
    page.add(range_slider)

ft.run(main)
```

**属性说明：**
- `min` / `max`：最小/最大值
- `start_value` / `end_value`：起始/结束值
- `divisions`：分割段数
- `label`：标签格式，`{value}` 会被替换为当前值
- `on_change_start`：开始拖动时触发
- `on_change`：拖动过程中触发
- `on_change_end`：拖动结束时触发

---

### TimePicker - 时间选择器

时间选择对话框控件。

```python
import flet as ft
from datetime import time

def main(page: ft.Page):
    def handle_change(e):
        print(f"时间变化: {e.control.value}")
        
    def handle_dismissal(e):
        print("时间选择器关闭")
    
    time_picker = ft.TimePicker(
        value=time(hour=19, minute=30),
        confirm_text="确认",
        cancel_text="取消",
        help_text="选择时间段",
        entry_mode=ft.TimePickerEntryMode.DIAL,  # 或 INPUT
        on_change=handle_change,
        on_dismiss=handle_dismissal,
    )
    
    # 显示时间选择器
    def show_time_picker(e):
        page.overlay.append(time_picker)
        time_picker.open = True
        page.update()
    
    page.add(
        ft.Button("选择时间", on_click=show_time_picker)
    )

ft.run(main)
```

**属性说明：**
- `value`：初始时间值（datetime.time 对象）
- `confirm_text`：确认按钮文本
- `cancel_text`：取消按钮文本
- `help_text`：帮助文本
- `entry_mode`：输入模式（DIAL 或 INPUT）
- `on_change`：时间变化时触发
- `on_dismiss`：关闭时触发

---

## 列表控件

### ReorderableListView - 可重排序列表

支持拖拽排序的列表视图。

```python
import flet as ft

def main(page: ft.Page):
    items = [f"Item {i}" for i in range(10)]
    
    def handle_reorder(e):
        # e.old_index 和 e.new_index 表示拖拽前后的索引
        old_index = e.old_index
        new_index = e.new_index
        
        # 重新排序数据
        item = items.pop(old_index)
        items.insert(new_index, item)
        
        print(f"移动项目: {old_index} -> {new_index}")
        print(f"新顺序: {items}")
    
    reorderable_list = ft.ReorderableListView(
        show_default_drag_handles=True,  # 显示拖拽手柄
        on_reorder=handle_reorder,
        controls=[
            ft.ListTile(
                title=ft.Text(items[i]),
                leading=ft.ReorderableDragHandle(
                    content=ft.Icon(ft.Icons.DRAG_INDICATOR),
                ),
            )
            for i in range(len(items))
        ],
    )
    
    page.add(reorderable_list)

ft.run(main)
```

**属性说明：**
- `show_default_drag_handles`：是否显示默认拖拽手柄
- `on_reorder`：重新排序时触发，提供 `old_index` 和 `new_index`
- `controls`：列表项，使用 `ReorderableDragHandle` 标记可拖拽项

---

### Dismissible - 可滑动删除项

支持滑动删除的列表项容器。

```python
import flet as ft

def main(page: ft.Page):
    items = [f"Item {i}" for i in range(5)]
    
    def handle_dismiss(e):
        print(f"项目被滑动: {e.control.content.title.value}")
        
    def handle_confirm_dismiss(e):
        # 可以在这里确认是否允许删除
        print("确认删除")
        return True  # 返回 True 允许删除，False 取消
    
    def create_dismissible_item(text):
        return ft.Dismissible(
            content=ft.ListTile(title=ft.Text(text)),
            dismiss_direction=ft.DismissDirection.HORIZONTAL,  # 水平方向滑动
            background=ft.Container(
                content=ft.Icon(ft.Icons.DELETE, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN,
                alignment=ft.Alignment.CENTER_LEFT,
                padding=ft.Padding(left=20),
            ),
            secondary_background=ft.Container(
                content=ft.Icon(ft.Icons.DELETE_FOREVER, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED,
                alignment=ft.Alignment.CENTER_RIGHT,
                padding=ft.Padding(right=20),
            ),
            on_dismiss=handle_dismiss,
            on_confirm_dismiss=handle_confirm_dismiss,
        )
    
    list_view = ft.ListView(
        controls=[create_dismissible_item(item) for item in items],
    )
    
    page.add(list_view)

ft.run(main)
```

**属性说明：**
- `content`：主要内容
- `dismiss_direction`：滑动方向（HORIZONTAL, VERTICAL, START_TO_END, END_TO_START）
- `background`：滑动时显示的背景（左侧/上方）
- `secondary_background`：次级背景（右侧/下方）
- `on_dismiss`：滑动删除后触发
- `on_confirm_dismiss`：确认是否允许删除

---

## 菜单控件

### MenuBar - 菜单栏

桌面应用风格的菜单栏，支持级联子菜单。

```python
import flet as ft

def main(page: ft.Page):
    def handle_menu_click(e):
        print(f"菜单点击: {e.control.content.value}")
    
    menu_bar = ft.MenuBar(
        expand=True,
        style=ft.MenuStyle(
            alignment=ft.Alignment.TOP_LEFT,
            bgcolor=ft.Colors.SURFACE,
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("文件"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("新建"),
                        leading=ft.Icon(ft.Icons.NEW_LABEL),
                        on_click=handle_menu_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("打开"),
                        leading=ft.Icon(ft.Icons.FOLDER_OPEN),
                        on_click=handle_menu_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("保存"),
                        leading=ft.Icon(ft.Icons.SAVE),
                        on_click=handle_menu_click,
                    ),
                    ft.Divider(),
                    ft.MenuItemButton(
                        content=ft.Text("退出"),
                        leading=ft.Icon(ft.Icons.EXIT_TO_APP),
                        on_click=lambda e: page.window.close(),
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("编辑"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("剪切"),
                        leading=ft.Icon(ft.Icons.CONTENT_CUT),
                        on_click=handle_menu_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("复制"),
                        leading=ft.Icon(ft.Icons.CONTENT_COPY),
                        on_click=handle_menu_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("粘贴"),
                        leading=ft.Icon(ft.Icons.CONTENT_PASTE),
                        on_click=handle_menu_click,
                    ),
                ],
            ),
        ],
    )
    
    page.add(menu_bar)

ft.run(main)
```

**属性说明：**
- `expand`：是否扩展填充可用空间
- `style`：菜单样式
- `controls`：菜单项列表，使用 `SubmenuButton` 创建子菜单

---

### SubmenuButton - 子菜单按钮

用于在菜单栏中创建级联子菜单。

```python
import flet as ft

# 基本用法
ft.SubmenuButton(
    content=ft.Text("文件"),
    controls=[
        ft.MenuItemButton(content=ft.Text("新建")),
        ft.MenuItemButton(content=ft.Text("打开")),
        ft.MenuItemButton(content=ft.Text("保存")),
    ],
)

# 带图标的子菜单
ft.SubmenuButton(
    content=ft.Row([
        ft.Icon(ft.Icons.SETTINGS),
        ft.Text("设置"),
    ]),
    controls=[
        ft.MenuItemButton(
            content=ft.Text("常规"),
            leading=ft.Icon(ft.Icons.SETTINGS_APPLICATIONS),
        ),
        ft.MenuItemButton(
            content=ft.Text("外观"),
            leading=ft.Icon(ft.Icons.COLOR_LENS),
        ),
    ],
)
```

---

### PopupMenuButton - 弹出菜单按钮

点击后弹出菜单的按钮控件。

```python
import flet as ft

def main(page: ft.Page):
    def handle_menu_click(e):
        print(f"菜单点击: {e.control.content}")
    
    popup_menu = ft.PopupMenuButton(
        icon=ft.Icon(ft.Icons.MORE_VERT),
        tooltip="更多选项",
        items=[
            ft.PopupMenuItem(
                content=ft.Text("Item 1"),
                on_click=handle_menu_click,
            ),
            ft.PopupMenuItem(
                icon=ft.Icon(ft.Icons.POWER_INPUT),
                content=ft.Text("检查电源"),
                on_click=handle_menu_click,
            ),
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.HOURGLASS_TOP_OUTLINED),
                    ft.Text("自定义内容"),
                ]),
                on_click=handle_menu_click,
            ),
            ft.PopupMenuItem(),  # 分隔线
            ft.PopupMenuItem(
                content=ft.Text("删除", color=ft.Colors.RED),
                on_click=handle_menu_click,
            ),
        ],
    )
    
    page.add(popup_menu)

ft.run(main)
```

**属性说明：**
- `icon`：按钮图标
- `tooltip`：提示文本
- `items`：菜单项列表

---

## 效果和工具控件

### Shimmer - 闪烁加载效果

用于骨架屏的闪烁加载动画效果。

```python
import flet as ft

def main(page: ft.Page):
    # 加载中的骨架屏效果
    shimmer = ft.Shimmer(
        base_color=ft.Colors.with_opacity(0.3, ft.Colors.GREY_400),
        highlight_color=ft.Colors.WHITE,
        content=ft.Column(
            controls=[
                ft.Container(
                    height=80,
                    bgcolor=ft.Colors.GREY_300,
                    border_radius=8,
                ),
                ft.Container(
                    height=80,
                    bgcolor=ft.Colors.GREY_300,
                    border_radius=8,
                ),
                ft.Container(
                    height=80,
                    bgcolor=ft.Colors.GREY_300,
                    border_radius=8,
                ),
            ],
            spacing=10,
        ),
    )
    
    page.add(shimmer)

ft.run(main)
```

**属性说明：**
- `base_color`：基础颜色（闪烁时较暗的颜色）
- `highlight_color`：高亮颜色（闪烁时较亮的颜色）
- `content`：需要添加闪烁效果的子控件

---

### Screenshot - 截图控件

用于捕获界面内容的控件。

```python
import flet as ft

def main(page: ft.Page):
    async def capture_screenshot(e):
        # 捕获截图
        image = await screenshot.capture()
        if image:
            # 显示截图
            screenshot_image.src = image
            page.update()
    
    # 创建可截图的控件
    screenshot = ft.Screenshot(
        ft.Container(
            ft.Button("Hello, world!", bgcolor=ft.Colors.BLUE),
            padding=10,
            bgcolor=ft.Colors.GREY_100,
        )
    )
    
    screenshot_image = ft.Image(width=200, height=100)
    
    page.add(
        ft.Text("原始控件:"),
        screenshot,
        ft.ElevatedButton("截图", on_click=capture_screenshot),
        ft.Text("截图结果:"),
        screenshot_image,
    )

ft.run(main)
```

**属性说明：**
- 传入需要截图的子控件
- `capture()` 方法异步返回截图的 base64 数据

---

### KeyboardListener - 键盘监听

专门用于监听键盘事件的控件。

```python
import flet as ft

def main(page: ft.Page):
    def key_down(e):
        print(f"按键按下: {e.key}")
        print(f"Shift: {e.shift}, Ctrl: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}")
        
        # 快捷键处理
        if e.ctrl and e.key == "S":
            print("保存快捷键")
        elif e.key == "Escape":
            print("退出")
            
    def key_up(e):
        print(f"按键释放: {e.key}")
    
    keyboard_listener = ft.KeyboardListener(
        content=ft.Container(
            content=ft.Text("点击此处后按键盘"),
            padding=50,
            bgcolor=ft.Colors.GREY_100,
        ),
        autofocus=True,
        on_key_down=key_down,
        on_key_up=key_up,
    )
    
    page.add(keyboard_listener)

ft.run(main)
```

**属性说明：**
- `content`：子控件
- `autofocus`：是否自动获取焦点
- `on_key_down`：按键按下时触发
- `on_key_up`：按键释放时触发
- 事件对象包含 `key`, `shift`, `ctrl`, `alt`, `meta` 属性

---

### SelectionArea - 可选中区域

使子控件内容可被用户选中的容器。

```python
import flet as ft

def main(page: ft.Page):
    selection_area = ft.SelectionArea(
        content=ft.Column([
            ft.Text("这段文字可以被选中", color=ft.Colors.GREEN),
            ft.Text("这段也可以被选中", color=ft.Colors.BLUE),
            ft.Container(
                content=ft.Text("容器内的文字同样可以被选中"),
                padding=20,
                bgcolor=ft.Colors.GREY_100,
            ),
        ])
    )
    
    page.add(
        ft.Text("尝试用鼠标选中下面的文字:"),
        selection_area,
    )

ft.run(main)
```

**属性说明：**
- `content`：子控件，其中的文本内容将可以被选中

---

### TransparentPointer - 透明指针

允许事件穿透到下层控件的容器。

```python
import flet as ft

def main(page: ft.Page):
    def bottom_click(e):
        print("下层按钮被点击!")
        
    def top_click(e):
        print("上层按钮被点击!")
    
    # 创建堆叠控件
    stack = ft.Stack(
        [
            # 下层按钮
            ft.Container(
                content=ft.Button("下层按钮", on_click=bottom_click),
                alignment=ft.Alignment.CENTER,
            ),
            # 透明指针层 - 事件会穿透到下层
            ft.TransparentPointer(
                content=ft.Container(
                    content=ft.Text("透明层（点击穿透到下层）"),
                    padding=50,
                    bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.RED),
                )
            ),
        ],
        width=400,
        height=200,
    )
    
    page.add(stack)

ft.run(main)
```

**属性说明：**
- `content`：子控件
- 事件会穿透该控件传递到下层控件

---

## 控件分类总结

### Material Design 3 按钮系列（4个）
| 控件 | 用途 |
|------|------|
| `FilledIconButton` | 填充图标按钮，主要操作 |
| `FilledTonalButton` | 填充色调按钮，次要强调 |
| `FilledTonalIconButton` | 填充色调图标按钮 |
| `OutlinedIconButton` | 边框图标按钮，次要操作 |

### 输入控件（5个）
| 控件 | 用途 |
|------|------|
| `SearchBar` | 搜索栏，支持实时搜索和建议 |
| `AutoComplete` | 自动完成输入框 |
| `DropdownM2` | MD3 风格下拉菜单 |
| `RangeSlider` | 范围滑块，选择区间 |
| `TimePicker` | 时间选择器对话框 |

### 列表控件（2个）
| 控件 | 用途 |
|------|------|
| `ReorderableListView` | 可拖拽重排序列表 |
| `Dismissible` | 可滑动删除的列表项 |

### 菜单控件（3个）
| 控件 | 用途 |
|------|------|
| `MenuBar` | 菜单栏，支持级联子菜单 |
| `SubmenuButton` | 子菜单按钮 |
| `PopupMenuButton` | 弹出菜单按钮 |

### 效果和工具控件（5个）
| 控件 | 用途 |
|------|------|
| `Shimmer` | 闪烁加载效果，骨架屏 |
| `Screenshot` | 截图控件 |
| `KeyboardListener` | 键盘事件监听 |
| `SelectionArea` | 可选中区域 |
| `TransparentPointer` | 透明指针，事件穿透 |

---

**文档版本**：Flet >= 0.82.0
**新增控件数量**：19个
**最后更新**：2026年3月
