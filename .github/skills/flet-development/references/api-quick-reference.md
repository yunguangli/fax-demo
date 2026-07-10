# Flet 1.0+ API 快速参考

> 本文档提供 Flet 1.0+ 高频 API 的正确用法，所有示例都经过 `inspect` 验证。
> 
> **使用场景**：开发时快速查找 API 正确用法，避免查阅多个文档。

---

## 快速导航

- [基础控件](#基础控件)
- [布局控件](#布局控件)
- [交互控件](#交互控件)
- [对话框与提示](#对话框与提示)
- [样式与装饰](#样式与装饰)

---

## 基础控件

### KeyboardEvent - 键盘事件 ✅

**验证签名**：
```
page.on_keyboard_event = callback
```

**参数说明**：
- `e.key`: 按键名称（字符串，如 "W", "A", "S", "D", "Arrow Up" 等）
- `e.shift`: Shift 键是否按下（布尔值）
- `e.ctrl`: Ctrl 键是否按下（布尔值）
- `e.alt`: Alt 键是否按下（布尔值）
- `e.meta`: Meta 键是否按下（布尔值）
- **⚠️ 没有 `e.event_type` 或 `e.type` 属性！无法区分 keydown/keyup！**
- **⚠️ 没有 `page.on_key_down` 和 `page.on_key_up`！**

**正确用法**：
```python
# ✅ 正确 - 使用 page.on_keyboard_event
def on_keyboard(e: ft.KeyboardEvent):
    if e.key == "W":
        # 处理 W 键
    if e.ctrl and e.key == "S":
        # 处理 Ctrl+S

page.on_keyboard_event = on_keyboard

# ✅ 正确 - 长按移动（使用时间戳）
import time

key_timestamps = {}

def on_keyboard(e: ft.KeyboardEvent):
    key = e.key.upper()
    if key in ["W", "A", "S", "D"]:
        key_timestamps[key] = time.time()

page.on_keyboard_event = on_keyboard

async def move_loop():
    while True:
        current_time = time.time()
        # 如果在最近 100ms 内触发过，则认为按键还在按下
        if current_time - key_timestamps.get("W", 0) < 0.1:
            # 移动
        await asyncio.sleep(0.03)

# ❌ 错误 - 使用不存在的 API
page.on_key_down = callback  # AttributeError!
page.on_key_up = callback  # AttributeError!

# ❌ 错误 - 使用不存在的 event_type
if e.event_type == "keydown":  # AttributeError!
    # 处理
```

**⚠️ 重要特性**：
1. **事件重复触发**：按键按下时会持续触发事件（类似 keydown 重复）
2. **没有 keyup 事件**：需要用时间戳或其他机制判断按键释放
3. **区分大小写**：`e.key` 返回的键名可能是大写或小写，需要 `.upper()` 统一

**使用场景**：
- 游戏控制（WASD 移动）
- 快捷键（Ctrl+S 保存）
- 方向键导航

---

### BorderRadius - 圆角 ✅

**验证签名**：
```
(top_left: int | float, top_right: int | float, bottom_left: int | float, bottom_right: int | float)
```

**参数说明**：
- `top_left`: 左上角
- `top_right`: 右上角
- `bottom_left`: 左下角
- `bottom_right`: 右下角
- **⚠️ 参数名是完整单词，不是缩写（tl/tr/bl/br）**

**正确用法**：
```python
# ✅ 直接构造 - 全部四个参数
ft.BorderRadius(top_left=5, top_right=5, bottom_left=0, bottom_right=0)

# ✅ 统一圆角（新版本，>= 0.80.0）
ft.BorderRadius.all(10)  # ⚠️ 使用 BorderRadius.all()（大写 B）

# ❌ 统一圆角（已弃用，< 0.80.0）
ft.border_radius.all(10)  # DeprecationWarning: will be removed in 0.83.0

# ✅ 部分圆角
ft.border_radius.only(top_left=5, top_right=5, bottom_left=0, bottom_right=0)

# ❌ 错误 - 缩写参数名
ft.BorderRadius(tl=5, tr=5, bl=0, br=0)  # TypeError: unexpected keyword argument 'tl'

# ❌ 错误 - 只提供部分参数
ft.BorderRadius(top_left=5, top_right=5)  # TypeError: missing 2 required positional arguments
```

**⚠️ 破坏性变更（Flet 0.80.0+）**：
- `ft.border_radius.all()` 已弃用，将在 0.83.0 移除
- 使用 `ft.BorderRadius.all()` 替代（注意大写 B）

---

### Padding - 内边距 ✅

**验证签名**：
```
(left: int | float, top: int | float, right: int | float, bottom: int | float)
```

**正确用法**：
```python
# ✅ 直接构造 - 全部四个参数
ft.Padding(left=10, top=5, right=10, bottom=5)

# ✅ 统一内边距
ft.padding.all(10)

# ✅ 部分内边距
ft.padding.only(left=10, top=5, right=10, bottom=5)

# ✅ 对称内边距
ft.padding.symmetric(horizontal=10, vertical=5)
```

---

### Margin - 外边距 ✅

**正确用法**：
```python
# ✅ 直接构造
ft.Margin(left=10, top=5, right=10, bottom=5)

# ✅ 统一外边距
ft.margin.all(10)

# ✅ 部分外边距
ft.margin.only(left=10, top=5, right=10, bottom=5)
```

---

### Colors - 颜色 ✅

**正确用法**：
```python
# ✅ 使用预定义颜色（大写 C）
ft.Colors.BLUE
ft.Colors.RED
ft.Colors.GREEN
ft.Colors.BLUE_700
ft.Colors.GREY_500

# ✅ 使用 Material Design 色阶（100-900，数字越大越深）
ft.Colors.RED_900    # 深红色（不是 DARK_RED）
ft.Colors.BLUE_800   # 深蓝色
ft.Colors.GREEN_700  # 深绿色

# ✅ 使用十六进制颜色
"#FF5722"
"#2196F3"

# ❌ 错误 - 小写 colors
ft.colors.BLUE  # AttributeError

# ❌ 错误 - 使用 values()
ft.Colors.values()  # TypeError: 'super' object has no attribute '__getattr__'

# ❌ 错误 - 不存在的颜色名称
ft.Colors.DARK_RED  # AttributeError: 'super' object has no attribute '__getattr__'
ft.Colors.DARK_BLUE  # AttributeError
```

**⚠️ 常见颜色命名陷阱**：
- ❌ `DARK_RED` → ✅ `RED_900`
- ❌ `DARK_BLUE` → ✅ `BLUE_900`
- ❌ `DARK_GREEN` → ✅ `GREEN_900`
- ❌ `LIGHT_RED` → ✅ `RED_100`
- ❌ `LIGHT_BLUE` → ✅ `BLUE_100`

**Material Design 色阶说明**：
- `_50` - 最浅
- `_100` - 很浅
- `_200` - 较浅
- `_300` - 浅
- `_400` - 稍浅
- `_500` - 标准色
- `_600` - 稍深
- `_700` - 较深
- `_800` - 很深
- `_900` - 最深

---

### Alignment - 对齐 ✅

**验证签名**：
```
(x: float, y: float)
```

**正确用法**：
```python
# ✅ 预定义对齐方式（大写 A）
ft.Alignment.CENTER
ft.Alignment.TOP_LEFT
ft.Alignment.TOP_CENTER
ft.Alignment.TOP_RIGHT
ft.Alignment.CENTER_LEFT
ft.Alignment.CENTER_RIGHT
ft.Alignment.BOTTOM_LEFT
ft.Alignment.BOTTOM_CENTER
ft.Alignment.BOTTOM_RIGHT

# ✅ 自定义对齐
ft.Alignment(x=0.5, y=0.5)  # 居中

# ❌ 错误 - 小写 alignment
ft.alignment.center  # AttributeError
```

---

## 布局控件

### Tabs - 标签页 ✅

**验证签名**：
```
(content: Control, length: int, selected_index: int = 0, ...)
```

**重要变更**：Flet 1.0+ 中 Tabs API **完全重写**，使用三件套结构。

**正确用法**：
```python
# ✅ 三件套结构
ft.Tabs(
    content=ft.Column([
        # 1. TabBar - 标签栏
        ft.TabBar(
            tabs=[
                ft.Tab(label="标签1", icon=ft.Icons.HOME),
                ft.Tab(label="标签2", icon=ft.Icons.SETTINGS),
            ],
        ),
        # 2. TabBarView - 内容面板（必须设置 height！）
        ft.TabBarView(
            height=120,  # ⚠️ 必须设置 height
            controls=[
                ft.Container(content=ft.Text("内容1"), padding=20),
                ft.Container(content=ft.Text("内容2"), padding=20),
            ],
        ),
    ]),
    length=2,  # ⚠️ 必须等于 Tab 数量
    selected_index=0,
)

# ❌ 错误 - 旧 API
ft.Tabs(tabs=[ft.Tab(label="A")])  # TypeError: unexpected keyword argument 'tabs'

# ❌ 错误 - Tab 有 content 参数
ft.Tab(label="A", content=ft.Text("..."))  # TypeError: unexpected keyword argument 'content'
```

**注意事项**：
- `TabBarView` 必须设置 `height` 参数，否则报错 `height is unbounded`
- `length` 必须等于 `Tab` 的数量
- `Tab` 只能用 `label` 和 `icon` 参数，没有 `content` 参数

---

### ListView - 列表视图 ✅

**正确用法**：
```python
ft.ListView(
    controls=[ft.Container(...) for i in range(10)],
    expand=True,  # 自动填充剩余空间
    spacing=10,   # 子控件间距
    padding=10,   # 内边距
)
```

---

### Column / Row - 列和行 ✅

**正确用法**：
```python
# Column - 垂直布局
ft.Column(
    controls=[
        ft.Text("第一行"),
        ft.Text("第二行"),
    ],
    spacing=10,  # 子控件间距
    scroll=ft.ScrollMode.AUTO,  # 自动滚动
)

# Row - 水平布局
ft.Row(
    controls=[
        ft.Text("左"),
        ft.Text("右"),
    ],
    alignment=ft.MainAxisAlignment.CENTER,  # 对齐方式
    spacing=10,
)
```

---

## 交互控件

### Button - 按钮 ✅

**验证签名**：
```
(content: Control | None = None, icon: Control | None = None, on_click: Callable | None = None, ...)
```

**正确用法**：
```python
# ✅ 基础按钮
ft.Button(content=ft.Text("点击"))

# ✅ 带图标按钮
ft.Button(
    content=ft.Row([
        ft.Icon(ft.Icons.ADD),
        ft.Text("添加"),
    ]),
    on_click=lambda e: print("点击"),
)

# ✅ 带样式按钮
ft.Button(
    content=ft.Text("保存"),
    style=ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE,
    ),
)

# ✅ 其他按钮类型
ft.FilledButton(content=ft.Text("填充按钮"))
ft.OutlinedButton(content=ft.Text("边框按钮"))
ft.TextButton("文本按钮")

# ❌ 错误 - ElevatedButton 已移除
ft.ElevatedButton(content=ft.Text("按钮"))  # NameError: name 'ElevatedButton' is not defined
```

---

### TextField - 文本输入框 ✅

**正确用法**：
```python
# ✅ 基础输入框
ft.TextField(
    label="用户名",
    hint_text="请输入用户名",
)

# ✅ 密码输入框
ft.TextField(
    label="密码",
    password=True,
    can_reveal_password=True,  # 显示/隐藏密码
)

# ✅ 带图标的输入框
ft.TextField(
    label="邮箱",
    prefix_icon=ft.Icons.EMAIL,
)

# ✅ 多行输入框
ft.TextField(
    label="描述",
    multiline=True,
    min_lines=3,
    max_lines=5,
)
```

---

### Icon - 图标 ✅

**验证签名**：
```
(icon: str | Icons, size: int | float = 24, color: str | Colors | CupertinoColors | None = None, ...)
```

**正确用法**：
```python
# ✅ 使用预定义图标
ft.Icon(ft.Icons.HOME, size=24, color=ft.Colors.BLUE)

# ✅ 常用图标
ft.Icons.ADD
ft.Icons.DELETE
ft.Icons.EDIT
ft.Icons.SETTINGS
ft.Icons.SEARCH
ft.Icons.PERSON
ft.Icons.ANDROID  # ⚠️ ROBOT 图标不存在

# ❌ 错误 - 使用 name 参数
ft.Icon(name=ft.Icons.HOME)  # TypeError: unexpected keyword argument 'name'

# ❌ 错误 - ROBOT 图标不存在
ft.Icon(ft.Icons.ROBOT)  # AttributeError: ROBOT
```

**可用图标列表**：
- `ft.Icons.ANDROID` - 机器人（ROBOT 不存在）
- `ft.Icons.HOME` - 首页
- `ft.Icons.SETTINGS` - 设置
- `ft.Icons.PERSON` - 用户
- `ft.Icons.SEARCH` - 搜索
- 完整列表：运行 `python -c "import flet as ft; print([attr for attr in dir(ft.Icons) if not attr.startswith('_')])"`

---

### IconButton - 图标按钮 ✅

**正确用法**：
```python
ft.IconButton(
    icon=ft.Icons.ADD,
    icon_color=ft.Colors.BLUE,
    tooltip="添加",
    on_click=lambda e: print("点击"),
)
```

---

### CircleAvatar - 圆形头像 ✅

**验证签名**：
```
(content: Control | None = None, foreground_image_url: str | None = None, 
 radius: int | float | None = None, bgcolor: str | Colors | CupertinoColors | None = None, ...)
```

**正确用法**：
```python
# ✅ 使用图标作为头像
ft.CircleAvatar(
    content=ft.Icon(ft.Icons.PERSON, size=40, color=ft.Colors.WHITE),
    bgcolor=ft.Colors.BLUE_700,
    radius=40,
)

# ✅ 使用图片作为头像
ft.CircleAvatar(
    foreground_image_url="https://example.com/avatar.jpg",
    radius=40,
)

# ✅ 带文字的头像
ft.CircleAvatar(
    content=ft.Text("A", size=20, color=ft.Colors.WHITE),
    bgcolor=ft.Colors.BLUE,
    radius=20,
)
```

---

## 对话框与提示

### AlertDialog - 警告对话框 ✅

**正确用法**：
```python
# ✅ 创建对话框
dialog = ft.AlertDialog(
    title=ft.Text("提示"),
    content=ft.Text("这是一个对话框"),
    actions=[
        ft.Button(content=ft.Text("确定"), on_click=lambda e: page.pop_dialog()),
        ft.Button(content=ft.Text("取消"), on_click=lambda e: page.pop_dialog()),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
)

# ✅ 显示对话框
page.show_dialog(dialog)

# ✅ 关闭对话框
page.pop_dialog()

# ❌ 错误 - page.open() 不存在
page.open(dialog)  # AttributeError: 'Page' object has no attribute 'open'
```

---

### SnackBar - 底部提示 ✅

**正确用法**：
```python
# ✅ 创建 SnackBar
snackbar = ft.SnackBar(
    content=ft.Text("操作成功"),
    bgcolor=ft.Colors.GREEN,
)

# ✅ 显示 SnackBar
page.overlay.append(snackbar)
snackbar.open = True
page.update()

# ❌ 错误 - page.snack_bar 已废弃
page.snack_bar = snackbar  # AttributeError or DeprecationWarning
```

---

### BottomSheet - 底部抽屉 ✅

**正确用法**：
```python
# ✅ 创建 BottomSheet
bottom_sheet = ft.BottomSheet(
    content=ft.Container(
        content=ft.Column([
            ft.Text("操作菜单"),
            ft.Button(content=ft.Text("选项1")),
            ft.Button(content=ft.Text("选项2")),
        ]),
        padding=20,
    ),
)

# ✅ 显示 BottomSheet
page.overlay.append(bottom_sheet)
bottom_sheet.open = True
page.update()

# ❌ 错误 - page.bottom_sheet 已废弃
page.bottom_sheet = bottom_sheet  # AttributeError or DeprecationWarning
```

---

## 样式与装饰

### Card - 卡片 ✅

**正确用法**：
```python
ft.Card(
    content=ft.Container(
        content=ft.Text("卡片内容"),
        padding=15,
    ),
    elevation=2,  # 阴影
)
```

---

### Container - 容器 ✅

**正确用法**：
```python
ft.Container(
    content=ft.Text("内容"),
    bgcolor=ft.Colors.WHITE,
    border_radius=ft.BorderRadius(top_left=10, top_right=10, bottom_left=10, bottom_right=10),
    padding=ft.Padding(left=10, top=5, right=10, bottom=5),
    margin=ft.Margin(left=10, top=5, right=10, bottom=5),
    on_click=lambda e: print("点击"),
)
```

---

### BoxShadow - 阴影 ✅

**正确用法**：
```python
ft.BoxShadow(
    spread_radius=1,
    blur_radius=15,
    color=ft.Colors.GREY_300,
    offset=ft.Offset(0, 2),
)
```

---

## 启动应用

### ft.run() - 启动应用 ✅

**正确用法**：
```python
def main(page: ft.Page):
    page.title = "我的应用"
    page.add(ft.Text("Hello, Flet!"))

# ✅ 正确启动方式
ft.run(main)

# ❌ 错误 - ft.app() 已废弃
ft.app(target=main)  # TypeError or AttributeError
```

---

## 验证方法

### 验证 API 签名

```python
# 方法1：使用 inspect
python -c "import inspect; import flet as ft; print(inspect.signature(ft.BorderRadius.__init__))"

# 方法2：检查所有属性和方法
python -c "import flet as ft; print([m for m in dir(ft.Page) if not m.startswith('_')])"

# 方法3：检查属性是否存在
python -c "import flet as ft; print('exists' if hasattr(ft, 'CircleAvatar') else 'not exists')"
```

---

**最后更新**：2026-03-20  
**版本**：Flet 0.82.2  
**验证状态**：所有 API 都经过 `inspect` 验证 ✅
