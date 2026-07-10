# Flet 1.0+ 常见错误排查指南

> 本文档提供 Flet 1.0+ 开发中常见错误的解决方案。

---

## 高频错误（按出现频率排序）

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Tabs.__init__() got an unexpected keyword argument 'tabs'` | Tabs API 完全重写 | 用 `Tabs(content=..., length=N)` + `TabBar` + `TabBarView` |
| `Tabs.__init__() missing 2 required positional arguments: 'content' and 'length'` | Tabs 需要 content 和 length | 见下方三件套写法 |
| `Tab.__init__() got an unexpected keyword argument 'content'` | Tab 没有 `content` 参数 | `ft.Tab(label=..., icon=...)` |
| `Badge.__init__() got an unexpected keyword argument 'label_style'` | Badge 只能用 `label` 参数 | `ft.Badge(label="5")` **只用label！** |
| `Badge.__init__() got an unexpected keyword argument 'small'` | Badge 只能用 `label` 参数 | `ft.Badge(label="5")` **只用label！** |
| `Unknown control: Badge` | Badge 不能直接在 Stack 中使用 | 用 `Container + Text` 替代 |
| `'super' object has no attribute '__getattr__'` | 使用了 `ft.Colors.values()` | 手动定义颜色列表，见下方 |
| `Radio must be enclosed within RadioGroup` | Radio 没有被 RadioGroup 包裹 | `ft.RadioGroup(content=ft.Radio(...))` |
| `Error displaying TabBarView: height is unbounded` | TabBarView 在无界高度容器中 | **直接给 `TabBarView` 设 `height=固定值`** |
| `TextButton.__init__() got an unexpected keyword argument 'text'` | 新版本不支持 text 参数 | 使用 `content` 参数 |
| `PopupMenuItem.__init__() got an unexpected keyword argument 'text'` | text 参数已移除 | `ft.PopupMenuItem(content=ft.Text(...))` |
| `'NavigationDrawer' object has no attribute 'open'` | 使用了 overlay.append() 或试图使用 open 属性 | 必须用 `page.drawer = drawer`，然后用 `await page.show_drawer()` / `close_drawer()` |
| 界面不实时更新 | 线程 + time.sleep 问题 | 改用 asyncio |
| `module 'flet.controls.alignment' has no attribute 'center'` | 小写 center 不存在 | 使用 `ft.Alignment.CENTER` |
| `'utf-8' codec can't encode characters` | 编码问题 | 添加编码声明，使用 datetime |
| `ft.colors.XXX`（小写 s）| 大小写写错 | `ft.Colors.XXX`（大写 C，单数）|
| `Icon.__init__() got an unexpected keyword argument 'name'` | name 属性已弃用 | 使用 `icon` 属性 |
| `NameError: name 'ElevatedButton' is not defined` | ElevatedButton 已移除 | 使用 `ft.Button(...)` 或 `ft.FilledButton(...)` |
| `'Window' object has no attribute 'transparent'` | Flet 1.0+ 已移除 transparent 属性 | 该属性已完全移除，透明窗口需用替代方案 |
| `coroutine 'Window.center' was never awaited` | `window.center()` 是异步方法 | 改用 `await page.window.center()` |
| `clipboard is deprecated since version 0.80.0` | `page.clipboard` 已弃用 | 改用 `clipboard = ft.Clipboard()` |
| `module 'flet' has no attribute 'Audio'` | ft.Audio 控件已完全移除 | 使用 pygame/pydub 等第三方库 |
| `Dropdown.__init__() got unexpected keyword argument 'on_change'` | 参数名已变更 | 改用 `on_select` |
| `module 'flet' has no attribute 'PaintStyle'` | 枚举名已变更 | 改用 `ft.PaintingStyle` |
| `module 'flet.canvas' has no attribute 'Polygon'` | Polygon 控件已移除 | 改用 `ft.canvas.Path` |
| `Paint.__init__() got unexpected keyword argument 'stroke_dash'` | 参数名已变更 | 改用 `stroke_dash_pattern` |
| `'Path' object has no attribute 'move_to'` | Path 构建方式已变更 | 改用 `elements=[Path.MoveTo(...)]` |
| `BorderRadius.__init__() missing 2 required positional arguments` | BorderRadius 需要全部四个参数 | 改用 `BorderRadius(top_left=5, top_right=5, bottom_left=0, bottom_right=0)` |
| `coroutine 'Window.close' was never awaited` | `window.close()` 是异步方法 | 改用 `await page.window.close()` |
| `Draggable.__init__() got unexpected keyword argument 'on_drag_end'` | 参数名已变更 | 改用 `on_drag_complete` |
| `'DragUpdateEvent' object has no attribute 'local_x'` | 属性名已变更 | 改用 `e.local_position.x` |
| `TypeError: unsupported operand type(s) for -: 'NoneType' and 'float'` | `max_width/max_height` 可能为 None | 使用默认值如 `page.window.max_width or 1920` |
| `AttributeError: 'Page' object has no attribute 'client_storage'` | client_storage 已弃用 | 使用 `ft.SharedPreferences()` 类 |
| 异步应用无法启动或报错 | 使用了 `ft.app(target=main)` | 使用 `ft.run(main)` |
| `app() missing required argument: 'target'` | 缺少参数名 | 使用 `ft.run(main)` |
| `handler must be a coroutine function` | 事件处理器中使用了 await 但不是异步函数 | 使用 `async def` 定义事件处理器 |
| 动画无效果（悬停/点击） | 动画属性的事件处理器需要 async | 推荐使用 `async def` |
| 淡入淡出无效果 | 使用了错误的动画属性 | 使用 `animate_opacity` 而非 `animate` |
| 旋转动画无效果 | 使用了错误的动画属性 | 使用 `animate_rotation` 而非 `animate` |
| 悬停事件不触发 | `e.data == "true"` 字符串比较 | Flet 1.0+ 中 `e.data` 是布尔值，直接用 `if e.data:` |
| `Page has no attribute 'bottom_sheet'` | `page.bottom_sheet` 属性已废弃 | 使用 `page.overlay.append(bottom_sheet)` |
| `Page has no attribute 'snack_bar'` | `page.snack_bar` 属性已废弃 | 使用 `page.overlay.append(snackbar)` |
| BottomSheet 不显示 | 使用了 `page.bottom_sheet` 属性 | 添加到 `page.overlay` 并设置 `open=True` |
| SnackBar 不显示 | 使用了 `page.snack_bar` 属性 | 添加到 `page.overlay` 并设置 `open=True` |

---

## 详细错误说明

### 1. Tabs 控件完全重写（高频！重大变更！）

**错误信息：**
```
TypeError: Tabs.__init__() got an unexpected keyword argument 'tabs'
TypeError: Tab.__init__() got an unexpected keyword argument 'content'
TypeError: Tabs.__init__() missing 2 required positional arguments: 'content' and 'length'
```

**原因：**
Flet 1.0+ 中 Tabs 控件 API **完全重写**，旧 API 100% 不可用。新的 API 使用 `Tabs + TabBar + TabBarView` 三件套。

**解决方案：**
```python
# ❌ 旧 API - 全部报错！
ft.Tabs(tabs=[ft.Tab(label="A"), ft.Tab(label="B")])  # 报错：没有 tabs 参数
ft.Tab(label="A", content=ft.Text("..."))              # 报错：没有 content 参数

# ✅ 新 API - 三件套结构
ft.Tabs(
    content=ft.Column([
        ft.TabBar(                    # 标签栏
            tabs=[                     # Tab 项列表
                ft.Tab(label="标签1", icon=ft.Icons.HOME),
                ft.Tab(label="标签2", icon=ft.Icons.SETTINGS),
            ],
        ),
        ft.TabBarView(                # 内容面板 - ⚠️ 必须设 height！
            height=120,                # ✅ 直接给 TabBarView 设 height
            controls=[                 # 每个 Tab 对应的内容
                ft.Container(content=ft.Text("内容1"), padding=20),
                ft.Container(content=ft.Text("内容2"), padding=20),
            ],
        ),
    ]),
    length=2,              # 必须指定 Tab 数量
    selected_index=0,
)
```

**API 对照：**
| 旧 API | 新 API |
|--------|--------|
| `ft.Tabs(tabs=[...])` | `ft.Tabs(content=..., length=N)` |
| `ft.Tab(text=..., content=...)` | `ft.Tab(label=..., icon=...)` |
| 无 | `ft.TabBar(tabs=[...])` - 标签栏 |
| 无 | `ft.TabBarView(controls=[...])` - 内容面板 |

---

### 2. Badge 控件参数错误（高频！）

**错误信息：**
```
TypeError: Badge.__init__() got an unexpected keyword argument 'label_style'
TypeError: Badge.__init__() got an unexpected keyword argument 'small'
TypeError: Badge.__init__() got an unexpected keyword argument 'text_color'
TypeError: Badge.__init__() got an unexpected keyword argument 'bgcolor'
Unknown control: Badge
```

**原因：**
Flet 1.0+ 中 Badge 控件大幅简化，**只能使用 `label` 参数**，其他所有样式参数都已移除。此外，**Badge 不能直接在 Stack 中作为独立控件使用**。

**解决方案：**
```python
# ❌ 错误写法 - 这些参数全部无效！
ft.Badge(label="5", label_style=ft.TextStyle(size=12))  # 报错！
ft.Badge(label="5", small=True)                       # 报错！
ft.Badge(label="5", text_color=ft.Colors.WHITE)       # 报错！
ft.Badge(label="5", bgcolor=ft.Colors.RED)            # 报错！

# ✅ 正确写法 - 只能使用 label 参数
ft.Badge(label="5")
ft.Badge(label="新")

# ❌ 错误：Badge 不能直接在 Stack 中使用
ft.Stack([
    ft.Container(
        content=ft.Badge(label="新"),  # 报错：Unknown control: Badge
        right=10,
        top=10,
    ),
])

# ✅ 正确：在 Stack 中使用 Container + Text 组合替代 Badge
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
)

# ✅ 如需自定义样式，使用 Container + Text 组合
ft.Container(
    content=ft.Text("5", color=ft.Colors.WHITE, size=12),
    bgcolor=ft.Colors.RED,
    border_radius=10,
    padding=ft.Padding(4, 2, 4, 2),
)
```

---

### 3. Colors 枚举遍历错误（高频！）

**错误信息：**
```
AttributeError: 'super' object has no attribute '__getattr__'
```

**原因：**
`ft.Colors` 枚举没有 `values()` 方法，不能遍历或动态获取颜色。

**解决方案：**
```python
# ❌ 错误写法 - Colors 没有 values() 方法
colors = ft.Colors.values()                    # 报错！
color = ft.Colors.values()[index]              # 报错！
for c in ft.Colors.values():                   # 报错！
    print(c)

# ✅ 正确写法 - 手动定义颜色列表
COLOR_PALETTE = [
    ft.Colors.RED, ft.Colors.BLUE, ft.Colors.GREEN,
    ft.Colors.ORANGE, ft.Colors.PURPLE, ft.Colors.CYAN,
    ft.Colors.PINK, ft.Colors.TEAL, ft.Colors.AMBER,
]
selected_color = COLOR_PALETTE[index % len(COLOR_PALETTE)]

# ✅ 直接使用具体颜色
ft.Container(bgcolor=ft.Colors.BLUE)
```

---

### 4. Radio 必须包裹在 RadioGroup 中（高频！）

**错误信息：**
```
Radio must be enclosed within RadioGroup
```

**原因：**
`ft.Radio` 控件不能单独使用，必须包裹在 `ft.RadioGroup` 中。

**解决方案：**
```python
# ❌ 错误写法 - Radio 直接使用
ft.Radio(value="1", label="单选")

# ✅ 正确写法 - 用 RadioGroup 包裹
ft.RadioGroup(
    value="1",
    content=ft.Radio(value="1", label="单选"),
)

# ✅ 正确写法 - 多个 Radio 在同一个 RadioGroup 中
ft.RadioGroup(
    value="option_a",
    content=ft.Column([
        ft.Radio(value="option_a", label="选项A"),
        ft.Radio(value="option_b", label="选项B"),
        ft.Radio(value="option_c", label="选项C"),
    ]),
)
```

---

### 5. TabBarView 高度无界错误（高频！）

**错误信息：**
```
Error displaying TabBarView: height is unbounded. Set a fixed height, a non-zero expand, or place it inside a control with bounded height.
```

**原因：**
`TabBarView` 放在无界高度的容器中（如 `ft.Column(scroll=...)`、`ft.ListView`），底层是 Flutter 的 `PageView`，需要从父级获得确切的高度约束。

**解决方案：**
```python
# ❌ 错误写法 - TabBarView 没有设置自身的 height
ft.Tabs(
    content=ft.Column([
        ft.TabBar(tabs=[ft.Tab(label="标签1"), ft.Tab(label="标签2")]),
        ft.TabBarView(controls=[
            ft.Container(content=ft.Text("内容1"), padding=20),
        ]),
    ]),
    length=2,
)

# ✅ 最可靠方案：直接给 TabBarView 设置 height 属性
ft.Tabs(
    content=ft.Column([
        ft.TabBar(tabs=[ft.Tab(label="标签1"), ft.Tab(label="标签2")]),
        ft.TabBarView(
            height=120,  # ✅ 直接设 height！
            controls=[
                ft.Container(content=ft.Text("内容1"), padding=20),
                ft.Container(content=ft.Text("内容2"), padding=20),
            ],
        ),
    ]),
    length=2,
)
```

---

### 6. PopupMenuItem 参数错误

**错误：**
```
TypeError: PopupMenuItem.__init__() got an unexpected keyword argument 'text'
```

**原因：**
Flet 1.0+ 中 `ft.PopupMenuItem` 移除了 `text` 参数，必须使用 `content` 参数。

**解决方案：**
```python
# ❌ Flet 0.x 写法 - Flet 1.0+ 报错
ft.PopupMenuItem(text="个人资料")

# ✅ Flet 1.0+ 写法
ft.PopupMenuItem(content=ft.Text("个人资料"))

# ✅ 带图标的菜单项
ft.PopupMenuItem(
    icon=ft.Icon(ft.Icons.SETTINGS),
    content=ft.Text("设置"),

---

### 7. BorderRadius 参数错误（高频！易错！）

**错误信息：**
```
TypeError: BorderRadius.__init__() got an unexpected keyword argument 'tl'
TypeError: BorderRadius.__init__() missing 2 required positional arguments: 'bottom_left' and 'bottom_right'
```

**原因：**
1. **参数名错误**：使用了缩写 `tl/tr/bl/br`，但实际参数名是完整单词 `top_left/top_right/bottom_left/bottom_right`
2. **参数缺失**：Flet 1.0+ 要求必须提供全部四个参数，不支持部分参数

**解决方案：**
```python
# ❌ 错误写法1 - 使用了缩写参数名
ft.BorderRadius(tl=5, tr=5, bl=0, br=0)  # 报错：unexpected keyword argument 'tl'

# ❌ 错误写法2 - 只提供部分参数
ft.BorderRadius(top_left=5, top_right=5)  # 报错：missing 2 required positional arguments

# ✅ 正确写法 - 全部四个参数，使用完整参数名
ft.BorderRadius(top_left=5, top_right=5, bottom_left=0, bottom_right=0)

# ✅ 正确写法 - 使用便捷函数（新版本，>= 0.80.0）
ft.BorderRadius.all(10)  # 四个角统一圆角（大写 B）

# ❌ 旧版本（已弃用，将在 0.83.0 移除）
ft.border_radius.all(10)  # DeprecationWarning

# ✅ 正确写法 - 只设置部分圆角
ft.border_radius.only(top_left=5, top_right=5, bottom_left=0, bottom_right=0)
```

**⚠️ 重点记忆：**
- 参数名是 **完整单词**：`top_left`/`top_right`/`bottom_left`/`bottom_right`
- **不是缩写**：`tl`/`tr`/`bl`/`br`（这些会报错！）
- 必须提供全部四个参数

---
)
```

---

### 7. NavigationDrawer open 属性错误

**错误：**
```
AttributeError: 'NavigationDrawer' object has no attribute 'open'
```

**原因：**
1. 使用了 `page.overlay.append(drawer)` 而不是 `page.drawer = drawer`
2. 或者试图使用 `drawer.open` 或 `page.drawer.open` 属性

**关键结论：NavigationDrawer 没有 `open` 属性！**

**解决方案：**
```python
# ❌ 错误写法 - 使用 overlay
page.overlay.append(drawer)  # NavigationDrawer 不能放 overlay

# ❌ 错误写法 - 使用 open 属性
drawer.open = True          # 报错：'NavigationDrawer' object has no attribute 'open'
page.drawer.open = True     # 同样报错！

# ✅ 正确写法 - 必须使用 page.drawer
drawer = ft.NavigationDrawer(...)
page.drawer = drawer  # 关键：设置到 page.drawer

# ✅ 然后用 await page.show_drawer() / close_drawer() 控制
async def toggle_drawer():
    await page.show_drawer()   # 打开
    # 或
    await page.close_drawer()  # 关闭
```

**注意：**
- NavigationDrawer 必须通过 `page.drawer`（左侧）或 `page.end_drawer`（右侧）设置
- **不能用** `page.overlay.append()` 方式
- **不能用** `open` 属性，必须用 `await page.show_drawer()` / `await page.close_drawer()`
- 事件处理器必须是 `async def`

---

### 8. Window.transparent 属性移除

**错误：**
```
AttributeError: 'Window' object has no attribute 'transparent'
```

**原因：**
Flet 1.0+ 中 `page.window.transparent` 属性已被完全移除，同时 `ft.run(transparent_window=True)` 启动参数也已失效。

**解决方案：**
```python
# ❌ 错误写法 - Flet 0.x 方式（已失效）
page.window.transparent = True
ft.run(main, transparent_window=True)

# ✅ 替代方案 - Flet 1.0+ （效果可能因平台而异）
page.bgcolor = ft.Colors.TRANSPARENT
# 注意：transparent_window 启动参数已不可用
```

**注意：**
- `page.window.transparent` 属性已完全移除，无法访问
- `ft.run(transparent_window=True)` 启动参数已失效
- 透明窗口效果在 Flet 1.0+ 中可能需要平台特定的配置

---

### 1. 按钮控件错误

**错误：**
```
TypeError: TextButton.__init__() got an unexpected keyword argument 'text'
```

**原因：**
Flet 1.0+ 中 Button 类控件不再支持 `text` 参数，必须使用 `content` 参数。

**解决方案：**
```python
# ❌ 错误写法
ft.TextButton(text="点击我")

# ✅ 正确写法
ft.TextButton(content=ft.Text("点击我"))

# ✅ TextButton 也可以直接使用字符串
ft.TextButton("点击我")
```

---

### 2. 对齐方式错误

**错误：**
```
AttributeError: module 'flet.controls.alignment' has no attribute 'center'
```

**原因：**
对齐常量需要使用大写的 `Alignment.CENTER`，而不是小写的 `alignment.center`。

**解决方案：**
```python
# ❌ 错误写法
alignment=ft.alignment.center

# ✅ 正确写法
alignment=ft.Alignment.CENTER
```

---

### 3. 编码错误

**错误：**
```
'utf-8' codec can't encode characters in position 1-9: surrogates not allowed
```

**原因：**
在某些系统上使用 `time.strftime()` 包含中文时出现编码错误。

**解决方案：**
```python
# ✅ 在文件开头添加编码声明
# -*- coding: utf-8 -*-

# ✅ 使用 datetime.now() 替代 time.strftime()
from datetime import datetime

# ✅ 手动映射中文星期
weekday_map = {
    0: "星期一", 1: "星期二", 2: "星期三",
    3: "星期四", 4: "星期五", 5: "星期六", 6: "星期日"
}

now = datetime.now()
weekday_cn = weekday_map[now.weekday()]
date_str = f"{now.strftime('%Y年%m月%d日')} {weekday_cn}"
```

---

### 4. 图标控件属性错误

**错误：**
```
TypeError: Icon.__init__() got an unexpected keyword argument 'name'
```

**原因：**
Icon 控件的 `name` 属性已弃用，改为使用 `icon` 属性。

**解决方案：**
```python
# ❌ 错误写法
ft.Icon(name=ft.Icons.HOME)

# ✅ 正确写法
ft.Icon(icon=ft.Icons.HOME)
```

---

### 5. 存储控件错误

**错误：**
```
AttributeError: 'Page' object has no attribute 'client_storage'
```

**原因：**
`client_storage` 已弃用，需要使用 `ft.SharedPreferences()` 类。

**解决方案：**
```python
# ❌ 错误写法
page.client_storage.set("key", "value")

# ✅ 正确写法
prefs = ft.SharedPreferences()
page.services.append(prefs)
await prefs.set("key", "value")
```

---

### 6. 应用启动错误

**错误：**
```
TypeError: app() missing required argument: 'target'
```

**原因：**
Flet 1.0+ 启动方式从 `ft.app(target=main)` 改为 `ft.run(main)`。

**解决方案：**
```python
# ❌ 错误写法
ft.app(target=main)

# ✅ 正确写法
ft.run(main)
```

---

### 7. 协程函数错误

**错误：**
```
The application encountered an error: handler must be a coroutine function
```

**原因：**
事件处理器中使用了 `await` 或调用了异步 API，但函数没有使用 `async def` 定义。

**解决方案：**
```python
# ❌ 错误写法
def on_click(e):
    files = await file_picker.pick_files()  # 错误：在同步函数中使用 await

# ✅ 正确写法
async def on_click(e):
    files = await file_picker.pick_files()
```

---

### 8. 动画属性错误

**错误：**
动画无效果（悬停/点击时控件属性变化无动画过渡）。

**原因：**
动画属性设置错误，或者事件处理器没有使用 `async def`。

**解决方案：**
```python
# ❌ 错误写法 - 使用 animate 属性对 opacity 无效
container = ft.Container(
    opacity=1.0,
    animate=300,  # 对 opacity 无效
)

# ✅ 正确写法 - 使用专门的动画属性
container = ft.Container(
    opacity=1.0,
    animate_opacity=300,  # 正确
)

# ✅ 事件处理器使用 async def
async def on_click(e):
    container.opacity = 0.5
    page.update()
```

---

### 9. 悬停事件错误

**错误：**
悬停事件不触发或判断逻辑错误。

**原因：**
Flet 1.0+ 中 `e.data` 是布尔值 `True/False`，不再是字符串 `"true"/"false"`。

**解决方案：**
```python
# ❌ 错误写法（旧版本）
def on_hover(e):
    if e.data == "true":  # 错误的字符串比较
        container.bgcolor = ft.Colors.BLUE

# ✅ 正确写法（新版本）
def on_hover(e):
    if e.data:  # 直接判断布尔值
        container.bgcolor = ft.Colors.BLUE
    else:
        container.bgcolor = ft.Colors.GREY
    page.update()
```

---

### 10. BottomSheet/SnackBar 显示错误

**错误：**
```
AttributeError: 'Page' object has no attribute 'bottom_sheet'
```

**原因：**
`page.bottom_sheet` 和 `page.snack_bar` 属性已废弃，需要使用 `page.overlay.append()`。

**解决方案：**
```python
# ❌ 错误写法（旧版本）
page.bottom_sheet = ft.BottomSheet(content=container)
page.bottom_sheet.open = True
page.update()

# ✅ 正确写法（新版本）
bottom_sheet = ft.BottomSheet(content=container)
page.overlay.append(bottom_sheet)
bottom_sheet.open = True
page.update()
```

---

## 控制台警告

| 警告信息 | 原因 | 解决方案 |
|---------|------|---------|
| `libpng warning: iCCP: known incorrect sRGB profile` | Flutter 内置图标资源的 PNG 文件包含非标准 ICC 配置文件 | **可以忽略**，无功能影响，纯粹是控制台噪音。可在程序入口添加 `warnings.filterwarnings("ignore", "(?s).*iCCP.*")` 抑制显示 |
| `ElevatedButton is not defined` | ElevatedButton 已移除 | 使用 `ft.Button` 或 `ft.FilledButton` |

---

## 控件属性错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Tab.__init__() got an unexpected keyword argument 'content'` | Tab 没有 `content` 参数 | 只用 `label` 参数，内容单独放 |
| `Badge.__init__() got an unexpected keyword argument 'label_style'` | Badge 只能使用 `label` 参数 | **只用 `ft.Badge(label="5")`，其他参数全无效！** |
| `Badge.__init__() got an unexpected keyword argument 'small'` | Badge 只能使用 `label` 参数 | **只用 `ft.Badge(label="5")`，其他参数全无效！** |
| `Unknown control: Badge` | Badge 不能直接在 Stack 中使用 | 用 `Container + Text` 替代 |
| `Badge.__init__() got an unexpected keyword argument 'text'` | text 属性已弃用 | 使用 `label` 属性 |
| `'super' object has no attribute '__getattr__'` | 使用了 `ft.Colors.values()` | 手动定义颜色列表，见下方 |
| `'Card' object has no attribute 'color'` | color 属性已弃用 | 使用 `bgcolor` 属性 |
| `Checkbox.__init__() got an unexpected keyword argument 'is_error'` | is_error 属性已弃用 | 使用 `error` 属性 |
| `'Switch' object has no attribute 'label_style'` | label_style 已弃用 | 使用 `label_text_style` |
| `'Tabs' object has no attribute 'is_secondary'` | is_secondary 已弃用 | 使用 `secondary` 属性 |
| `'BoxDecoration' object has no attribute 'shadow'` | shadow 单数已弃用 | 使用 `shadows` 复数形式 |

---

## 参数和方法错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `'Padding' object has no attribute 'symmetric'` | Padding 不支持 symmetric | 使用命名参数 `left/right/top/bottom` |
| `scroll_to() got an unexpected keyword argument 'key'` | key 参数已弃用 | 使用 `scroll_key` 参数 |
| `SegmentedButton selected type error` | selected 类型错误 | 使用 `List[str]` 替代 `Set` |
| `method '_async' not found` | 方法名已变更 | 移除 `_async` 后缀 |
| `type object 'FontWeight' has no attribute 'MEDIUM'` | FontWeight 枚举变更 | 使用 `FontWeight.W_500` 替代 `MEDIUM` |
| `invalid literal for int() with base 10` | 类型转换失败 | 添加输入验证，捕获 ValueError |
| `get_keys() missing 1 required positional argument` | get_keys 需要 key_prefix 参数 | 传入空字符串 `get_keys("")` |

---

## 服务和存储错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `'FilePicker' object has no attribute 'pick_files'` | FilePicker 未添加到服务 | 添加到 `page.services` |
| `'list' object has no attribute 'files'` | pick_files 返回值格式变更 | 直接使用返回的 list，无需 `.files` |
| `'str' object has no attribute 'path'` | save_file/get_directory 返回值格式变更 | 返回值本身就是路径字符串 |
| `'Theme' object has no attribute 'primary_swatch'` | primary_swatch 已移除 | 使用 `color_scheme_seed` |
| `ElevatedButton is not defined` | ElevatedButton 已移除 | 使用 `ft.Button` 或 `ft.FilledButton` |
| `DeprecationWarning: all() is deprecated` | border.all() 已废弃 | 使用 `ft.Border.all()` 替代 |
| `DeprecationWarning: shared_preferences is deprecated` | page.shared_preferences 已废弃 | 使用 `ft.SharedPreferences()` 类 |

---

## 事件错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `on_resized event not triggered` | 事件名称错误 | 使用 `on_resize` 替代 `on_resized` |
| `DragTarget event data not available` | 事件对象字段变更 | 使用 `e.accept` 替代 `e.data` |
| `scroll_to() got unexpected argument 'key'` | 参数名称错误 | 使用 `scroll_key` 替代 `key` |

---

## 布局错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| ListView 性能问题 | 长列表未优化 | 使用 `item_extent` 固定项高度 |
| GridView 列数不对 | 未正确配置 | 使用 `runs_count` 或 `max_extent` |
| 响应式布局不生效 | 断点配置错误 | 检查 col 参数格式 `{"sm": 6, "md": 4}` |

---

## 常见错误速查表

### 属性变更速查

| 控件 | 旧属性 | 新属性 |
|-----|--------|--------|
| Icon | `name` | `icon` |
| Badge | `text` | `label` |
| Tabs | `text`, `tab_content` | `label` |
| Card | `color` | `bgcolor` |
| Card | `is_semantic_container` | `semantic_container` |
| Checkbox | `is_error` | `error` |
| Switch | `label_style` | `label_text_style` |
| Tabs | `is_secondary` | `secondary` |
| Chip | `click_elevation` | `press_elevation` |
| Markdown | `img_error_content` | `image_error_content` |
| NavigationRailDestination | `label_content` | `label` |
| Pagelet | `bottom_app_bar` | `bottom_appbar` |
| Canvas Text | `text` | `value` |
| CupertinoActionSheetAction | `is_default_action` | `default` |
| SafeArea | `left`, `top`... | `avoid_intrusions_*` |

### 枚举类型速查

| 类别 | 旧版本/错误 | 新版本/正确 |
|-----|------------|------------|
| 启动 | `ft.app(target=main)` | `ft.run(main)` |
| 对齐 | `ft.alignment.center` | `ft.Alignment.CENTER` |
| 适配 | `"contain"`, `ft.ImageFit.CONTAIN` | `ft.BoxFit.CONTAIN` |
| 颜色 | `"blue"`, `ft.colors.BLUE` | `ft.Colors.BLUE` |
| 字重 | `ft.FontWeight.MEDIUM` | `ft.FontWeight.W_500` |
| 动画 | - | `animate=300` 或 `ft.Animation(...)` |

### 动画属性速查

| 动画类型 | 旧版本 | 新版本 |
|---------|--------|--------|
| 通用动画 | `animate=...` | `animate=...` |
| 旋转动画 | `animate=...` + `ft.Rotate()` | `animate_rotation=...` + 弧度值 |
| 透明度动画 | `animate=...` | `animate_opacity=...` |
| 缩放动画 | `animate=...` | `animate_scale=...` |
| 位移动画 | `animate=...` | `animate_offset=...` |

---

**文档版本**：Flet >= 0.82.0
**最后更新**：2026年3月
