# Flet 1.0+ 破坏性变更详解

> 本文档包含 Flet 1.0+ (>=0.82.0) 的所有破坏性变更详细说明。

---

## 0. BorderRadius 创建方式变更 ⚠️ **重要**

**影响版本**：Flet >= 0.80.0
**移除版本**：Flet 0.83.0

**错误写法（已弃用）**：
```python
# ❌ 从 0.80.0 开始弃用，将在 0.83.0 移除
border_radius=ft.border_radius.all(10)
```

**正确写法**：
```python
# ✅ 使用 BorderRadius.all()（注意大写 B）
border_radius=ft.BorderRadius.all(10)

# ✅ 部分圆角仍然可以使用 border_radius.only
border_radius=ft.border_radius.only(top_left=5, top_right=5, bottom_left=0, bottom_right=0)

# ✅ 直接构造
border_radius=ft.BorderRadius(top_left=5, top_right=5, bottom_left=0, bottom_right=0)
```

**错误信息**：
```
DeprecationWarning: all() is deprecated since version 0.80.0 
and will be removed in version 0.83.0. Use BorderRadius.all() instead
```

**迁移指南**：
| 旧写法 | 新写法 |
|--------|--------|
| `ft.border_radius.all(10)` | `ft.BorderRadius.all(10)` |
| `ft.border_radius.all(5)` | `ft.BorderRadius.all(5)` |

**注意事项**：
- `border_radius.only()` 仍然可用
- `border_radius.symmetric()` 仍然可用
- 只有 `all()` 方法需要改为 `BorderRadius.all()`

---

## 1. 应用启动方式变更

**旧写法（V0.x 版本）：**
```python
# ❌ 旧版本使用 ft.app
ft.app(target=main)
```

**新写法（Flet 1.0 >= 0.80.0）：**
```python
# ✅ 使用 ft.run
ft.run(main)

# 或带参数
ft.run(main, view=ft.AppView.FLET_APP)
```

---

## 2. 按钮组件语法变更

**错误写法（旧版本）：**
```python
# ❌ ElevatedButton 已移除
ft.ElevatedButton(content=ft.Text("按钮"))

# ❌ TextButton 不支持 text 参数（但支持字符串作为第一个参数）
ft.TextButton(text="点击我")  # 错误：使用 text 参数
```

**正确写法（新版本）：**
```python
# ✅ TextButton 直接接受字符串参数
ft.TextButton("点击我")
ft.TextButton("Buy tickets")  # 官方文档示例

# ✅ OutlinedButton 仍然可用
ft.OutlinedButton(content=ft.Text("边框按钮"))

# ✅ FilledButton 用于主要操作
ft.FilledButton(content=ft.Text("保存"), icon=ft.Icons.SAVE)

# ✅ Button 是新的标准按钮
ft.Button(
    content=ft.Text("GitHub主页"),
    icon=ft.Icons.LINK,
    url="https://github.com/HnBigVolibear/",
)

# ✅ Button 带样式
ft.Button(
    content=ft.Text("保存"),
    style=ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREEN,
    ),
)
```

---

## 3. Alignment 对齐方式

**错误写法：**
```python
# ❌ 小写的 alignment.center 不存在
alignment=ft.alignment.center
```

**正确写法：**
```python
# ✅ 使用大写的 Alignment.CENTER
alignment=ft.Alignment.CENTER

# 其他常用对齐方式
ft.Alignment.TOP_LEFT
ft.Alignment.TOP_CENTER
ft.Alignment.TOP_RIGHT
ft.Alignment.CENTER_LEFT
ft.Alignment.CENTER
ft.Alignment.CENTER_RIGHT
ft.Alignment.BOTTOM_LEFT
ft.Alignment.BOTTOM_CENTER
ft.Alignment.BOTTOM_RIGHT
```

---

## 4. BoxFit 适配方式

**错误写法：**
```python
# ❌ 使用字符串或旧属性名
fit="contain"
fit=ft.ImageFit.CONTAIN
```

**正确写法：**
```python
# ✅ 使用 ft.BoxFit 枚举
image = ft.Image(
    src="photo.png",
    fit=ft.BoxFit.CONTAIN,  # 或 COVER, FILL, FIT_WIDTH, FIT_HEIGHT
    width=200,
    height=200,
)

# 常用 BoxFit 值：
# - CONTAIN: 保持比例，完整显示
# - COVER: 保持比例，填满容器
# - FILL: 拉伸填满
# - FIT_WIDTH: 宽度适配
# - FIT_HEIGHT: 高度适配
```

---

## 5. Border 边框设置

**错误写法（旧版本）：**
```python
# ❌ ft.border.all() 已废弃
border=ft.border.all(1, ft.Colors.GREY_300)
border=ft.border.only(
    left=ft.border.BorderSide(2, ft.Colors.BLUE),
)
```

**正确写法（新版本）：**
```python
# ✅ 使用 ft.Border.all()
border=ft.Border.all(1, ft.Colors.GREY_300)

# ✅ 单边框
border=ft.Border(
    left=ft.BorderSide(2, ft.Colors.BLUE),
    top=ft.BorderSide(2, ft.Colors.BLUE),
)
```

---

## 6. 颜色使用规范

**⚠️ 重要限制：`ft.Colors` 枚举没有 `values()` 方法，不能直接遍历或动态获取！**

**错误写法：**
```python
# ❌ 使用字符串（不推荐）
color="blue"
bgcolor="#FF5722"

# ❌ 使用旧版本的颜色常量
color=ft.colors.BLUE

# ❌ Colors 枚举没有 values() 方法，以下代码会报错！
colors_list = ft.Colors.values()  # 报错：'super' object has no attribute '__getattr__'

# ❌ 不能动态获取或遍历颜色
color = ft.Colors.values()[index]          # 报错！
for color in ft.Colors.values():           # 报错！
    print(color)
```

**正确写法：**
```python
# ✅ 使用 ft.Colors 枚举（推荐）
text = ft.Text("Hello", color=ft.Colors.BLUE)
container = ft.Container(bgcolor=ft.Colors.GREY_100)

# ✅ 常用颜色示例
ft.Colors.BLUE
ft.Colors.BLUE_700
ft.Colors.RED
ft.Colors.GREEN
ft.Colors.GREY_100
ft.Colors.TRANSPARENT

# ✅ 也可以使用十六进制（某些场景）
container = ft.Container(bgcolor="#E3F2FD")

# ✅ 需要颜色列表时，手动定义
COLOR_PALETTE = [
    ft.Colors.RED, ft.Colors.BLUE, ft.Colors.GREEN,
    ft.Colors.ORANGE, ft.Colors.PURPLE, ft.Colors.CYAN,
    ft.Colors.PINK, ft.Colors.TEAL, ft.Colors.AMBER,
]
selected_color = COLOR_PALETTE[index % len(COLOR_PALETTE)]

# ✅ 使用随机颜色（手动定义列表后随机选择）
import random
color = random.choice(COLOR_PALETTE)
```

**颜色最佳实践：**
- 优先使用 `ft.Colors` 枚举，保证类型安全
- **切记：`ft.Colors` 没有 `values()` 方法，不能遍历！**
- 需要颜色列表时，手动定义常量列表
- 使用带数字后缀的变体（如 `BLUE_700`）获得更多选择
- Material Design 颜色值：50, 100, 200, 300, 400, 500, 600, 700, 800, 900

---

## 7. 动画参数设置

**错误写法：**
```python
# ❌ 使用旧版本的 Animation 对象方式
animate=ft.Animation(300, "easeInOut")
```

**正确写法：**
```python
# ✅ 方式1：直接使用毫秒数（最简单）
container = ft.Container(
    bgcolor=ft.Colors.BLUE,
    animate=300,  # 300毫秒动画
)

# ✅ 方式2：使用 ft.Animation（需要更多控制时）
container = ft.Container(
    bgcolor=ft.Colors.BLUE,
    animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
)

# ✅ 常用动画曲线
ft.AnimationCurve.EASE_IN
ft.AnimationCurve.EASE_OUT
ft.AnimationCurve.EASE_IN_OUT
ft.AnimationCurve.BOUNCE_OUT
ft.AnimationCurve.ELASTIC_OUT
```

**动画最佳实践：**
- 简单场景直接用毫秒数
- 复杂动画才使用 `ft.Animation` 对象
- 常用时长：100-500ms（太长会影响用户体验）

---

## 8. Padding 和 Margin 参数变更

**错误写法（旧版本）：**
```python
# ❌ 不支持位置参数
container = ft.Container(
    padding=ft.Padding.symmetric(0, 10)
)
```

**正确写法（新版本）：**
```python
# ✅ 方式1：使用命名参数（推荐）
container = ft.Container(
    padding=ft.Padding(left=10, right=10, top=5, bottom=5)
)

# ✅ 方式2：使用 vertical/horizontal 参数
container = ft.Container(
    padding=ft.Padding(vertical=10, horizontal=20)
)

# ✅ 方式3：直接使用数字（四边相同）
container = ft.Container(
    padding=10
)

# ✅ 方式4：使用 Padding 类方法
container = ft.Container(
    padding=ft.Padding.symmetric(vertical=10, horizontal=20)
)

# ✅ Margin 用法相同
container = ft.Container(
    margin=ft.Margin(left=5, right=5, top=10, bottom=10)
)
```

---

## 9. Icon 控件属性重命名

**错误写法（旧版本）：**
```python
# ❌ name 属性已弃用
icon = ft.Icon(name=ft.Icons.HOME)
```

**正确写法（新版本）：**
```python
# ✅ 使用 icon 属性
icon = ft.Icon(icon=ft.Icons.HOME, size=24, color=ft.Colors.BLUE)
```

---

## 10. Badge 控件属性变更

**⚠️ 重要限制：Badge 控件在 Flet 1.0+ 中只能使用最基础的 `label` 参数，且不能直接在 Stack 中使用！**

**错误写法（旧版本/无效参数）：**
```python
# ❌ text 属性已弃用
badge = ft.Badge(text="5")

# ❌ 以下参数在 Flet 1.0+ 中都无效，会报错！
badge = ft.Badge(label="5", label_style=ft.TextStyle(size=12))      # 报错！
badge = ft.Badge(label="5", small=True)                             # 报错！
badge = ft.Badge(label="5", text_color=ft.Colors.WHITE)             # 报错！
badge = ft.Badge(label="5", bgcolor=ft.Colors.RED)                  # 报错！
badge = ft.Badge(label="5", label_visible=True)                     # 报错！

# ❌ Badge 不能直接在 Stack 中使用，会出现 "Unknown control: Badge" 错误
ft.Stack([
    ft.Container(
        content=ft.Badge(label="新"),  # 报错！
        right=10,
        top=10,
    ),
])
```

**正确写法（新版本）：**
```python
# ✅ 唯一正确的写法：只使用 label 参数
badge = ft.Badge(label="5")
badge = ft.Badge(label="新")
badge = ft.Badge(label="99+")

# ✅ 配合其他控件使用
ft.IconButton(
    icon=ft.Icons.NOTIFICATIONS,
    badge=ft.Badge(label="3")
)

# ✅ 如需在 Stack 中显示徽章效果，使用 Container + Text 组合
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

# ✅ 如需自定义徽章样式，使用 Container + Text 组合
ft.Container(
    content=ft.Text("5", color=ft.Colors.WHITE, size=12),
    bgcolor=ft.Colors.RED,
    border_radius=10,
    padding=ft.Padding(4, 2, 4, 2),
)
```

**说明：**
- Badge 控件在 Flet 1.0+ 中大幅简化，**只能使用 `label` 参数**
- `label_style`、`small`、`text_color`、`bgcolor`、`label_visible` 等参数全部移除
- **Badge 不能直接在 Stack 中作为独立控件使用**，会出现 `Unknown control: Badge` 错误
- Badge 通常配合 IconButton、Icon 等控件的 `badge` 属性使用
- 如需自定义样式或在 Stack 中使用徽章效果，请使用 `Container + Text` 组合实现

---

## 11. Tabs 控件完全重写（重大变更）

**⚠️ Flet 1.0+ 中 Tabs 控件 API 完全重写，旧 API 100% 不可用！**

### 旧 API（已完全移除）

```python
# ❌ 旧 API - 全部报错！
ft.Tabs(
    tabs=[                           # 报错：没有 tabs 参数
        ft.Tab(text="标签1"),        # 报错：text 已弃用
        ft.Tab(content=ft.Text("")), # 报错：没有 content 参数
    ],
    selected_index=0,
)
```

### 新 API（Tabs + TabBar + TabBarView 三件套）

```python
# ✅ 新 API 正确写法（直接给 TabBarView 设 height）
ft.Tabs(
    content=ft.Column([
        # 标签栏 - 放置 Tab 项
        ft.TabBar(
            tabs=[
                ft.Tab(label="首页", icon=ft.Icons.HOME),
                ft.Tab(label="设置", icon=ft.Icons.SETTINGS),
                ft.Tab(label="关于", icon=ft.Icons.INFO),
            ],
            scrollable=True,
        ),
        # 内容面板 - ⚠️ 必须给 TabBarView 设 height！
        ft.TabBarView(
            height=120,  # ✅ 直接设 height（最可靠！TabBarView 继承 LayoutControl）
            controls=[
                ft.Container(content=ft.Text("首页内容"), padding=20),
                ft.Container(content=ft.Text("设置内容"), padding=20),
                ft.Container(content=ft.Text("关于内容"), padding=20),
            ],
        ),
    ]),
    length=3,           # 必须指定 Tab 总数
    selected_index=0,   # 默认选中的 Tab 索引
)
```

### API 对照表

| 控件 | 参数 | 说明 |
|------|------|------|
| `ft.Tabs` | `content` (Control), `length` (int), `selected_index` (int) | 外层容器 |
| `ft.TabBar` | `tabs` (list[Tab]), `scrollable` (bool) | 标签栏 |
| `ft.TabBarView` | `controls` (list[Control]) | 内容面板 |
| `ft.Tab` | `label` (str/Control), `icon` (IconData) | 单个标签头 |

### 关键变更说明

1. **`ft.Tabs` 不再有 `tabs` 参数**，改为 `content` + `length`
2. **`ft.Tab` 不再有 `content`/`text`/`tab_content` 参数**，只用 `label` 和 `icon`
3. **新增 `ft.TabBar` 控件** - 用于放置标签头
4. **新增 `ft.TabBarView` 控件** - 用于放置标签内容面板
5. **`TabBarView.controls` 的长度必须等于 `Tabs.length`**
6. **`TabBar.tabs` 的长度必须等于 `Tabs.length`**
7. **⚠️ `TabBarView` 需要有界高度！** 最可靠方案：**直接给 `ft.TabBarView` 设 `height=固定值`**（它继承 LayoutControl）。在 scroll Column 中不能用 Container 包裹或 expand 解决。

---

## 12. 滚动方法参数变更

**错误写法（旧版本）：**
```python
# ❌ key 参数已弃用
list_view.scroll_to(key="item_1")
```

**正确写法（新版本）：**
```python
# ✅ 使用 scroll_key 参数
list_view.scroll_to(scroll_key="item_1")

# 或使用 ScrollKey
item = ft.Container(key=ft.ScrollKey("item_1"))
```

---

## 13. 对话框显示方式变更

**错误写法（旧版本）：**
```python
# ❌ page.open() 已弃用
page.open(dialog)
page.close(dialog)
```

**正确写法（新版本）：**
```python
# ✅ 使用 show_dialog 和 pop_dialog
page.show_dialog(dialog)
page.pop_dialog()

# 或使用 open 属性
dialog.open = True
page.update()
```

---

## 14. NavigationDrawer 位置设置

**正确写法：**
```python
# ✅ 左侧抽屉使用 page.drawer
page.drawer = ft.NavigationDrawer(
    on_dismiss=handle_dismissal,
    on_change=handle_change,
    controls=[
        ft.NavigationDrawerDestination(
            label="Item 1",
            icon=ft.Icons.DOOR_BACK_DOOR_OUTLINED,
        ),
    ],
)

# ✅ 显示左侧抽屉
async def handle_show_drawer():
    await page.show_drawer()

# ✅ 右侧抽屉使用 page.end_drawer
page.end_drawer = ft.NavigationDrawer(
    on_dismiss=handle_dismissal,
    on_change=handle_change,
    controls=[...],
)

# ✅ 显示右侧抽屉
async def handle_show_drawer():
    await page.show_end_drawer()

# ✅ 关闭抽屉
async def handle_close():
    await page.close_drawer()
```

**说明：**
- NavigationDrawer 没有 `position` 属性，通过 `page.drawer`（左侧）和 `page.end_drawer`（右侧）来控制位置
- **必须通过 `page.drawer = drawer` 设置**，不能使用 `page.overlay.append(drawer)`
- **NavigationDrawer 没有 `open` 属性**，控制开关必须使用：
  - `await page.show_drawer()` - 打开左侧抽屉
  - `await page.show_end_drawer()` - 打开右侧抽屉
  - `await page.close_drawer()` - 关闭抽屉
- 事件处理器必须使用 `async def`

---

## 15. Theme 颜色属性变更

**错误写法（旧版本）：**
```python
# ❌ primary_swatch 已移除
page.theme = ft.Theme(primary_swatch=ft.Colors.BLUE)
```

**正确写法（新版本）：**
```python
# ✅ 使用 color_scheme_seed
page.theme = ft.Theme(
    color_scheme_seed=ft.Colors.BLUE,
    use_material3=True
)
```

---

## 16. Page 事件名称变更

**错误写法（旧版本）：**
```python
# ❌ on_resized 已弃用
page.on_resized = handle_resize
```

**正确写法（新版本）：**
```python
# ✅ 使用 on_resize
page.on_resize = handle_resize
```

---

## 17. Dropdown 事件行为变更

**旧版本：**
```python
# ⚠️ on_change 在选择时触发
dropdown = ft.Dropdown(on_change=handle_change)
```

**新版本：**
```python
# ✅ on_change 在值变化时触发，on_select 在选择时触发
dropdown = ft.Dropdown(
    on_change=handle_value_change,  # 值改变时
    on_select=handle_select         # 用户选择时
)
```

---

## 18. FilePicker 服务化变更

**错误写法（旧版本）：**
```python
# ❌ FilePicker 不能直接使用
file_picker = ft.FilePicker(on_result=handle_result)
page.add(file_picker)
```

**正确写法（新版本）：**
```python
# ✅ FilePicker 作为服务添加到 page.services
file_picker = ft.FilePicker()
page.services.append(file_picker)

# 所有方法都是异步的
async def pick_files():
    files = await file_picker.pick_files()
    if files:
        print(f"选择了: {[f.name for f in files]}")
```

---

## 19. FilePicker 返回值格式变更

**错误写法（旧版本）：**
```python
# ❌ 旧版本返回对象，需要访问 .files 或 .path 属性
result = await file_picker.pick_files()
if result and result.files:
    files = result.files

path = await file_picker.save_file()
if path:
    save_path = path.path  # ❌ 错误：'str' object has no attribute 'path'
```

**正确写法（新版本）：**
```python
# ✅ 新版本直接返回值，无需访问属性

# pick_files() 直接返回 list[FilePickerFile]
files = await file_picker.pick_files(allow_multiple=True)
if files:
    for f in files:
        print(f"文件: {f.name}, 路径: {f.path}")

# pick_files() 单选也返回 list
files = await file_picker.pick_files(allow_multiple=False)
if files:
    file = files[0]
    print(f"选择了: {file.name}")

# save_file() 直接返回 str | None
path = await file_picker.save_file(file_name="doc.txt")
if path:
    print(f"保存到: {path}")  # path 就是字符串

# get_directory_path() 直接返回 str | None
path = await file_picker.get_directory_path()
if path:
    print(f"目录: {path}")  # path 就是字符串
```

---

## 20. 存储控件变更（重要）

**迁移路径：** `client_storage` → `page.shared_preferences` → `ft.SharedPreferences()` 类

**错误写法（旧版本）：**
```python
# ❌ client_storage 已弃用
page.client_storage.set("key", "value")

# ❌ page.shared_preferences 也已废弃
await page.shared_preferences.set("key", "value")
value = await page.shared_preferences.get("key")
```

**正确写法（新版本）：**
```python
# ✅ 使用 SharedPreferences 类
prefs = ft.SharedPreferences()
page.services.append(prefs)

await prefs.set("key", "value")
value = await prefs.get("key")
keys = await prefs.get_keys("")  # 空字符串获取所有键
```

---

## 21. Animation 导入方式变更

**错误写法（旧版本）：**
```python
# ❌ 从 ft.animation 导入
from flet.animation import Animation
animation = Animation(300, ft.AnimationCurve.EASE_IN)
```

**正确写法（新版本）：**
```python
# ✅ 直接使用 ft.Animation
animation = ft.Animation(300, ft.AnimationCurve.EASE_IN)

# 或使用毫秒数
container = ft.Container(
    animate=300,  # 等同于 ft.Animation(300)
    bgcolor=ft.Colors.BLUE
)
```

---

## 22. DragTarget 事件对象变更

**错误写法（旧版本）：**
```python
# ❌ 使用 e.data
def on_will_accept(e):
    data = e.data
```

**正确写法（新版本）：**
```python
# ✅ 使用 e.accept
def on_will_accept(e):
    accepted = e.accept

def on_leave(e):
    src_id = e.src_id
```

---

## 23. SafeArea 属性前缀变更

**错误写法（旧版本）：**
```python
# ❌ 直接使用方向属性
safe_area = ft.SafeArea(
    left=True,
    right=True
)
```

**正确写法（新版本）：**
```python
# ✅ 添加 avoid_intrusions_ 前缀
safe_area = ft.SafeArea(
    avoid_intrusions_left=True,
    avoid_intrusions_right=True,
    avoid_intrusions_top=True,
    avoid_intrusions_bottom=True
)
```

---

## 24. SegmentedButton selected 属性类型变更

**错误写法（旧版本）：**
```python
# ❌ selected 使用 Set 类型
button = ft.SegmentedButton(
    selected={"1", "4"}
)
```

**正确写法（新版本）：**
```python
# ✅ selected 使用 List[str] 类型
button = ft.SegmentedButton(
    selected=["1", "4"]
)
```

---

## 25. Card 控件属性变更

**错误写法（旧版本）：**
```python
# ❌ 旧属性名称
card = ft.Card(
    color=ft.Colors.BLUE,
    is_semantic_container=True
)
```

**正确写法（新版本）：**
```python
# ✅ 新属性名称
card = ft.Card(
    bgcolor=ft.Colors.BLUE,
    semantic_container=True
)
```

---

## 26. Checkbox 控件属性变更

**错误写法（旧版本）：**
```python
# ❌ is_error 属性已弃用
checkbox = ft.Checkbox(is_error=True)
```

**正确写法（新版本）：**
```python
# ✅ 使用 error 属性
checkbox = ft.Checkbox(error=True)
```

---

## 27. Switch 控件属性变更

**错误写法（旧版本）：**
```python
# ❌ label_style 属性已弃用
switch = ft.Switch(label_style=ft.TextStyle())
```

**正确写法（新版本）：**
```python
# ✅ 使用 label_text_style 属性
switch = ft.Switch(label_text_style=ft.TextStyle())
```

---

## 28. Tabs 的 secondary 属性变更

**错误写法（旧版本）：**
```python
# ❌ is_secondary 属性已弃用
tabs = ft.Tabs(is_secondary=True)
```

**正确写法（新版本）：**
```python
# ✅ 使用 secondary 属性
tabs = ft.Tabs(secondary=True)
```

---

## 29. BoxDecoration shadow 属性变更

**错误写法（旧版本）：**
```python
# ❌ shadow 单数形式已弃用
decoration = ft.BoxDecoration(
    shadow=ft.BoxShadow(color=ft.Colors.BLACK)
)
```

**正确写法（新版本）：**
```python
# ✅ 使用 shadows 复数形式
decoration = ft.BoxDecoration(
    shadows=[ft.BoxShadow(color=ft.Colors.BLACK)]
)
```

---

## 30. Chip 控件属性变更

**错误写法（旧版本）：**
```python
# ❌ click_elevation 属性已弃用
chip = ft.Chip(click_elevation=5)
```

**正确写法（新版本）：**
```python
# ✅ 使用 press_elevation 属性
chip = ft.Chip(press_elevation=5)
```

---

## 31. Markdown 控件属性变更

**错误写法（旧版本）：**
```python
# ❌ img_error_content 属性已弃用
md = ft.Markdown(img_error_content=ft.Text("Error"))
```

**正确写法（新版本）：**
```python
# ✅ 使用 image_error_content 属性
md = ft.Markdown(image_error_content=ft.Text("Error"))
```

---

## 32. NavigationRailDestination 属性变更

**错误写法（旧版本）：**
```python
# ❌ label_content 属性已弃用
dest = ft.NavigationRailDestination(
    label_content=ft.Text("Home")
)
```

**正确写法（新版本）：**
```python
# ✅ 使用 label 属性
dest = ft.NavigationRailDestination(
    label=ft.Text("Home")
)
```

---

## 33. Pagelet 控件属性变更

**错误写法（旧版本）：**
```python
# ❌ bottom_app_bar 属性已弃用
pagelet = ft.Pagelet(bottom_app_bar=app_bar)
```

**正确写法（新版本）：**
```python
# ✅ 使用 bottom_appbar 属性
pagelet = ft.Pagelet(bottom_appbar=app_bar)
```

---

## 34. ScrollableControl 属性变更

**错误写法（旧版本）：**
```python
# ❌ on_scroll_interval 属性已弃用
list_view = ft.ListView(on_scroll_interval=0.5)
```

**正确写法（新版本）：**
```python
# ✅ 使用 scroll_interval 属性
list_view = ft.ListView(scroll_interval=0.5)
```

---

## 35. Cupertino 控件属性变更

**错误写法（旧版本）：**
```python
# ❌ 旧属性名称
action = ft.CupertinoActionSheetAction(
    is_default_action=True,
    is_destructive_action=False
)
```

**正确写法（新版本）：**
```python
# ✅ 新属性名称
action = ft.CupertinoActionSheetAction(
    default=True,
    destructive=False
)

# 同样适用于：
# - CupertinoDialogAction
# - CupertinoContextMenuAction
```

---

## 36. Canvas Text 控件属性变更

**错误写法（旧版本）：**
```python
# ❌ text 属性已弃用
canvas_text = ft.canvas.Text(text="Hello")
```

**正确写法（新版本）：**
```python
# ✅ 使用 value 属性
canvas_text = ft.canvas.Text(value="Hello")
```

---

## 37. 异步方法后缀移除

**错误写法（旧版本）：**
```python
# ❌ 方法名带 _async 后缀
await some_method_async()
```

**正确写法（新版本）：**
```python
# ✅ 直接使用方法名（无后缀）
await some_method()

# 所有异步方法都不再有 _async 后缀
# 也移除了 fire-and-forget 版本（非异步版本）
```

---

## 38. FontWeight 字重属性变更

**错误写法（旧版本）：**
```python
# ❌ FontWeight.MEDIUM 已移除
ft.Text("示例", weight=ft.FontWeight.MEDIUM)
```

**正确写法（新版本）：**
```python
# ✅ 使用 W_100 - W_900 或 BOLD/NORMAL
text = ft.Text("示例", weight=ft.FontWeight.W_500)  # Medium 对应 W_500

# 可用的 FontWeight 值：
# - ft.FontWeight.NORMAL  (正常)
# - ft.FontWeight.BOLD    (粗体)
# - ft.FontWeight.W_100 到 ft.FontWeight.W_900 (字重级别)
```

**字重对应关系：**
| 描述 | 旧版本 | 新版本 |
|------|--------|--------|
| 细体 | `FontWeight.LIGHT` | `FontWeight.W_300` |
| 正常 | `FontWeight.NORMAL` | `FontWeight.W_400` 或 `FontWeight.NORMAL` |
| 中等 | `FontWeight.MEDIUM` | `FontWeight.W_500` |
| 半粗 | `FontWeight.SEMI_BOLD` | `FontWeight.W_600` |
| 粗体 | `FontWeight.BOLD` | `FontWeight.W_700` 或 `FontWeight.BOLD` |

---

## 39. 按钮控件变更（ElevatedButton 已移除）

**重要说明：**
- `ElevatedButton` - 已移除，使用 `ft.Button` 或 `ft.FilledButton` 替代
- `TextButton` - **仍然可用**，支持字符串参数
- `OutlinedButton` - **仍然可用**
- `FilledButton` - **仍然可用**，用于主要操作
- `Button` - 新的标准按钮控件

**错误写法（旧版本）：**
```python
# ❌ ElevatedButton 已移除
ft.ElevatedButton(content=ft.Text("按钮"))
```

**正确写法（新版本）：**
```python
# ✅ TextButton 直接接受字符串参数
ft.TextButton("文本按钮")
ft.TextButton("Buy tickets")  # 官方文档示例

# ✅ OutlinedButton 仍然可用
ft.OutlinedButton(content=ft.Text("边框按钮"))

# ✅ FilledButton 用于主要操作
ft.FilledButton(content=ft.Text("主要操作"))

# ✅ Button 是新的标准按钮
ft.Button(
    content=ft.Text("按钮"),
    icon=ft.Icons.SAVE,
)

# ✅ Button 带样式
ft.Button(
    content=ft.Text("保存"),
    style=ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE,
    ),
)
```

---

## 40. Border.all() 替代 border.all()

**错误写法（旧版本）：**
```python
# ❌ ft.border.all() 已废弃
container = ft.Container(
    border=ft.border.all(1, ft.Colors.GREY_300)
)
```

**正确写法（新版本）：**
```python
# ✅ 使用 ft.Border.all()
container = ft.Container(
    border=ft.Border.all(1, ft.Colors.GREY_300)
)
```

---

## 41. SharedPreferences 类替代 page.shared_preferences

**错误写法（旧版本）：**
```python
# ❌ page.shared_preferences 已废弃
await page.shared_preferences.set("key", "value")
value = await page.shared_preferences.get("key")
keys = await page.shared_preferences.get_keys()
```

**正确写法（新版本）：**
```python
# ✅ 创建 SharedPreferences 实例并添加到服务
prefs = ft.SharedPreferences()
page.services.append(prefs)

# ✅ 支持多种数据类型（v0.82.2+）
await prefs.set("name", "张三")           # 字符串
await prefs.set("age", 25)                # 整数
await prefs.set("score", 98.5)            # 浮点数
await prefs.set("active", True)           # 布尔值
await prefs.set("tags", ["python", "flet"])  # 列表（v0.82.2+）

# 读取数据
name = await prefs.get("name")     # 返回 "张三"
age = await prefs.get("age")       # 返回 25
score = await prefs.get("score")   # 返回 98.5
active = await prefs.get("active") # 返回 True
tags = await prefs.get("tags")     # 返回 ["python", "flet"]

# ✅ get_keys() 需要 key_prefix 参数，空字符串表示获取所有键
keys = await prefs.get_keys("")
```

**支持的数据类型（v0.82.2+）：**
| 类型 | 示例 | 说明 |
|-----|------|------|
| `str` | `"张三"` | 字符串 |
| `int` | `25` | 整数 |
| `float` | `98.5` | 浮点数 |
| `bool` | `True` / `False` | 布尔值 |
| `list[str]` | `["a", "b", "c"]` | 字符串列表（v0.82.2 新增） |

---

## 42. SharedPreferences.get_keys() 需要 key_prefix 参数

**错误写法（旧版本）：**
```python
# ❌ get_keys() 无参数调用
keys = await prefs.get_keys()
```

**正确写法（新版本）：**
```python
# ✅ 必须传入 key_prefix 参数
keys = await prefs.get_keys("")  # 空字符串表示获取所有键
keys = await prefs.get_keys("user_")  # 获取以 "user_" 开头的键
```

---

## 43. 事件处理器语法规范

**规则说明：**

| 场景 | 必须用 `async def` | 可以用 `def` |
|------|-------------------|--------------|
| 调用异步 API（FilePicker, SharedPreferences 等） | ✅ | ❌ |
| 使用 `await asyncio.sleep()` 延迟操作 | ✅ | ❌ |
| 动画属性变化（scale, rotate, opacity 等） | ✅ 推荐 | ⚠️ 可能报错 |
| 简单控件属性修改（value, bgcolor 等） | ✅ | ✅ |
| 简单打印/显示操作 | ✅ | ✅ |

**必须使用 async def 的场景：**
```python
# ✅ 调用异步 API
async def on_pick_file(e):
    files = await file_picker.pick_files()
    
# ✅ 使用延迟操作
async def on_click_delay(e):
    container.scale = 0.8
    page.update()
    await asyncio.sleep(0.1)  # 必须用 async def
    container.scale = 1.0
    page.update()

# ✅ 动画属性变化（推荐 async def，避免 "handler must be a coroutine function" 错误）
async def on_hover(e):
    if e.data:
        container.bgcolor = ft.Colors.BLUE
        container.width = 250
    page.update()
```

**可以使用同步函数的场景：**
```python
# ✅ 简单属性修改
def on_simple_click(e):
    text.value = "点击了"
    page.update()

# ✅ 简单打印
ft.Button(content=ft.Text("按钮"), on_click=lambda e: print("点击"))
```

**官方文档参考：**
- Flet 官方入门示例使用同步函数：`def minus_click(e):`
- Breaking Changes 说明：移除 `_async` 后缀，统一方法命名，不强制要求 async

**最佳实践建议：**
- 统一使用 `async def` 作为事件处理器，避免混淆和错误
- 只有在确实不需要异步操作且代码简洁时，才使用同步函数

---

## 44. 延迟操作必须使用 asyncio.sleep()

**错误写法（旧版本）：**
```python
# ❌ 使用 page.run_task + page.wait()
def on_click(e):
    container.scale = 0.8
    page.update()
    
    def restore():
        container.scale = 1.0
        page.update()
    
    page.run_task(lambda: (page.wait(100), restore()))

# ❌ 使用 threading + time.sleep()
import threading
import time

def delayed_update():
    time.sleep(1)
    page.update()

threading.Thread(target=delayed_update).start()
```

**正确写法（新版本）：**
```python
# ✅ 使用 async def + await asyncio.sleep()
async def on_click(e):
    container.scale = 0.8
    page.update()
    
    await asyncio.sleep(0.1)  # 100毫秒
    
    container.scale = 1.0
    page.update()
```

**错误信息：** `The application encountered an error: handler must be a coroutine function`

---

## 45. 旋转动画使用 animate_rotation 属性

**错误写法（旧版本）：**
```python
# ❌ 使用 ft.Rotate 对象
container = ft.Container(
    animate=ft.Animation(800, ft.AnimationCurve.EASE_IN_OUT),
)

def on_click_rotate(e):
    rotation_angle[0] += 360
    container.rotate = ft.Rotate(angle=rotation_angle[0] * 3.14159 / 180)
    page.update()
```

**正确写法（新版本）：**
```python
# ✅ 使用 animate_rotation 属性，rotate 直接赋弧度值
import math

container = ft.Container(
    animate_rotation=ft.Animation(800, ft.AnimationCurve.EASE_IN_OUT),
)

async def on_click_rotate(e):
    rotation_angle[0] += 360
    # 使用 math.radians() 或直接赋弧度值
    container.rotate = math.radians(rotation_angle[0])
    page.update()
```

**说明：**
- `rotate` 动画需要设置 `animate_rotation` 属性（不是 `animate`）
- `rotate` 属性直接接受弧度值（float），无需创建 `ft.Rotate` 对象
- 使用 `math.radians()` 将角度转换为弧度

---

## 46. 透明度动画使用 animate_opacity 属性

**错误写法（旧版本）：**
```python
# ❌ 透明度动画使用 animate 属性无效
container = ft.Container(
    opacity=1.0,
    animate=ft.Animation(600, ft.AnimationCurve.EASE_IN_OUT),  # 对 opacity 无效
)

def on_click(e):
    container.opacity = 0.2
    page.update()  # 立即变化，无淡入淡出效果
```

**正确写法（新版本）：**
```python
# ✅ 使用 animate_opacity 属性
container = ft.Container(
    opacity=1.0,
    animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_IN_OUT),
)

async def on_click(e):
    container.opacity = 0.2 if container.opacity == 1.0 else 1.0
    page.update()  # 有淡入淡出效果
```

**说明：** Flet 1.0+ 将动画属性细分为：
- `animate`：通用动画（size, bgcolor 等）
- `animate_rotation`：旋转动画
- `animate_opacity`：透明度动画
- `animate_scale`：缩放动画
- `animate_offset`：位移动画

---

## 47. BottomSheet 显示方式变更

**错误写法（旧版本）：**
```python
# ❌ page.bottom_sheet 属性已废弃
page.bottom_sheet = ft.BottomSheet(
    content=ft.Container(...),
)
page.bottom_sheet.open = True
page.update()
```

**正确写法（新版本）：**
```python
# ✅ 使用 page.overlay.append()
bottom_sheet = ft.BottomSheet(
    content=ft.Container(
        content=ft.Column([
            ft.Text("BottomSheet 内容"),
            ft.Button("关闭", on_click=lambda _: close_bottomsheet()),
        ]),
        padding=20,
    ),
)

# 添加到 overlay
page.overlay.append(bottom_sheet)
bottom_sheet.open = True
page.update()

# 关闭函数
def close_bottomsheet():
    bottom_sheet.open = False
    page.update()
```

**说明：** 使用 `page.overlay.append()` 添加 BottomSheet，`open` 属性控制显示/隐藏。

---

## 48. SnackBar 显示方式变更

**错误写法（旧版本）：**
```python
# ❌ page.snack_bar 属性已废弃
page.snack_bar = ft.SnackBar(
    content=ft.Text("提示信息"),
)
page.snack_bar.open = True
page.update()
```

**正确写法（新版本）：**
```python
# ✅ 使用 page.overlay.append()
snackbar = ft.SnackBar(
    content=ft.Text("提示信息"),
    bgcolor=ft.Colors.GREY_800,
)

# 显示 SnackBar
def show_snackbar():
    page.overlay.append(snackbar)
    snackbar.open = True
    page.update()

# 或简写
def show_snackbar_short():
    sb = ft.SnackBar(ft.Text("提示信息"))
    page.overlay.append(sb)
    sb.open = True
    page.update()
```

**说明:** 使用 `page.overlay.append()` 添加 SnackBar，`open` 属性控制显示/隐藏。

---

## 49. page.overlay 通用使用模式

Flet 1.0+ 中，BottomSheet、SnackBar、Banner、NavigationDrawer 等控件都通过 `page.overlay` 管理。

### 显示控件

```python
# 创建控件
bottom_sheet = ft.BottomSheet(content=container)
snackbar = ft.SnackBar(content=ft.Text("提示"))

# 添加到 overlay 并显示
page.overlay.append(bottom_sheet)
bottom_sheet.open = True
page.update()

# 或一次性创建并显示
def show_control(control):
    page.overlay.append(control)
    control.open = True
    page.update()
```

### 隐藏控件

```python
# 方法1：设置 open=False（保留在 overlay 中）
bottom_sheet.open = False
page.update()

# 方法2：从 overlay 移除
def close_and_remove(control):
    control.open = False
    page.update()
    # 可选：完全移除
    if control in page.overlay:
        page.overlay.remove(control)
        page.update()
```

### 检查控件是否显示

```python
# 检查控件是否在 overlay 中
if bottom_sheet in page.overlay:
    print("BottomSheet 已添加到 overlay")

# 检查是否打开
if bottom_sheet.open:
    print("BottomSheet 正在显示")
```

### 清理所有 overlay 控件

```python
# 关闭并清理所有 overlay 控件
for control in page.overlay[:]:
    if hasattr(control, 'open'):
        control.open = False
page.overlay.clear()
page.update()
```

---

## 50. scroll_to() 方法参数变更

**错误写法（旧版本）：**
```python
# ❌ 使用 key 参数
list_view.scroll_to(key="item_1")
```

**正确写法（新版本）：**
```python
# ✅ 使用 scroll_key 参数
list_view.scroll_to(scroll_key="item_1")

# 或使用 ScrollKey 标记控件
item = ft.Container(
    content=ft.Text("项目"),
    key=ft.ScrollKey("item_1"),  # 标记滚动位置
)
```

---

## 51. ResponsiveRow 响应式布局

**响应式列宽配置：**
```python
# ✅ 根据屏幕宽度自动调整列数
ft.ResponsiveRow(
    [
        ft.Container(
            content=ft.Text("响应式卡片"),
            bgcolor=ft.Colors.BLUE,
            padding=20,
            col={"sm": 6, "md": 4, "lg": 3},  # 不同屏幕宽度占不同列数
        ),
        ft.Container(
            content=ft.Text("固定宽度"),
            bgcolor=ft.Colors.GREEN,
            padding=20,
            col=6,  # 固定占 6 列（总共 12 列）
        ),
    ],
    spacing=10,
    run_spacing=10,
)
```

**响应式断点说明：**
| 断点 | 屏幕宽度 |
|------|----------|
| sm | < 576px |
| md | >= 576px |
| lg | >= 768px |
| xl | >= 992px |
| xxl | >= 1200px |

---

## 52. GridView 布局配置

**GridView 最佳实践：**
```python
# ✅ 固定每行项数
ft.GridView(
    controls=[...],
    runs_count=4,  # 每行 4 个
    spacing=10,
    run_spacing=10,
)

# ✅ 根据宽度自动计算列数
ft.GridView(
    controls=[...],
    max_extent=150,  # 每项最大宽度，自动计算列数
    child_aspect_ratio=1.0,  # 宽高比
    spacing=10,
    run_spacing=10,
)
```

---

## 53. ListView 性能优化

**固定项高度提升性能：**
```python
# ✅ 使用 item_extent 固定项高度（推荐用于长列表）
list_view = ft.ListView(
    controls=[...],
    item_extent=60,  # 固定每项高度 60px
    spacing=5,
    padding=10,
    height=400,
)

# ✅ 虚拟滚动 - 只渲染可见项
list_view = ft.ListView(
    controls=[...],
    item_extent=50,  # 必须设置固定高度
    first_item_prototype=True,  # 使用第一项作为原型
)
```

---

## 54. 窗口属性完整说明

**常用窗口属性：**
```python
# 尺寸
page.window.width = 800
page.window.height = 600

# 位置
page.window.left = 100
page.window.top = 100
# ⚠️ center() 是异步方法，需要 await
await page.window.center()

# 屏幕尺寸可能为 None，使用前需判断
screen_width = page.window.max_width or 1920
screen_height = page.window.max_height or 1080

# 状态
page.window.maximized = True  # 最大化
page.window.minimized = True  # 最小化
page.window.full_screen = True  # 全屏

# 行为
page.window.resizable = True  # 可调整大小
page.window.movable = True  # 可移动
page.window.always_on_top = False  # 始终置顶
page.window.visible = True  # 可见

# 透明窗口 ⚠️ Flet 1.0+ 已移除 transparent 属性
# ❌ 已失效: page.window.transparent = True
# ❌ 已失效: ft.run(main, transparent_window=True)
# 替代方案: page.bgcolor = ft.Colors.TRANSPARENT 配合平台特定配置

# 关闭窗口
page.window.close()
```

---

## 55. DataTable 表格配置

**DataTable 完整示例：**
```python
ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text("列1", weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("列2", weight=ft.FontWeight.BOLD)),
    ],
    rows=[
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("数据1")),
                ft.DataCell(ft.Text("数据2")),
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
)
```

---

## 56. GestureDetector 手势检测

**常用手势事件：**
```python
ft.GestureDetector(
    on_tap=lambda e: print("点击"),
    on_double_tap=lambda e: print("双击"),
    on_long_press_start=lambda e: print("长按开始"),
    on_long_press_end=lambda e: print("长按结束"),
    on_pan_start=lambda e: print(f"拖动开始: {e.local_x}"),
    on_pan_update=lambda e: print(f"拖动中: {e.local_x}, {e.local_y}"),
    on_pan_end=lambda e: print("拖动结束"),
    on_scale_start=lambda e: print("缩放开始"),
    on_scale_update=lambda e: print(f"缩放: {e.scale}"),
    drag_interval=50,  # 拖动事件间隔（毫秒）
    content=ft.Container(...),
)
```

---

## 57. Audio 控件服务化

**错误写法（旧版本）：**
```python
# ❌ Audio 控件直接添加到页面
audio = ft.Audio(src="music.mp3")
page.add(audio)
```

**正确写法（新版本）：**
```python
# ✅ Audio 需要添加到 page.services
audio = ft.Audio(
    src="https://example.com/music.mp3",
    autoplay=False,
    volume=1.0,
    on_loaded=lambda e: print("加载完成"),
    on_state_changed=lambda e: print(f"状态: {e.data}"),
)
page.services.append(audio)

# 播放控制
audio.play()
audio.pause()
audio.stop()
audio.seek(10000)  # 跳转到 10 秒
audio.release()    # 释放资源
```

---

## 58. Clipboard 剪贴板异步操作

**正确用法：**
```python
# ✅ clipboard 操作是异步的
async def copy_text(e):
    await page.clipboard.set("复制的内容")
    
async def paste_text(e):
    content = await page.clipboard.get()
    if content:
        print(f"粘贴: {content}")
```

---

## 59. 键盘事件处理

**键盘事件属性：**
```python
def on_keyboard(e: ft.KeyboardEvent):
    print(f"按键: {e.key}")
    print(f"Shift: {e.shift}, Ctrl: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}")
    
    # 快捷键示例
    if e.ctrl and e.key == "S":
        save_document()
    elif e.key == "Escape":
        close_dialog()

page.on_keyboard_event = on_keyboard
```

---

## 60. InteractiveViewer 缩放平移

**缩放平移容器：**
```python
viewer = ft.InteractiveViewer(
    content=ft.Image(src="large_image.png"),
    min_scale=0.5,
    max_scale=3.0,
    boundary_margin=ft.Margin.all(20),
    on_interaction_start=lambda e: print("开始交互"),
    on_interaction_update=lambda e: print(f"缩放: {e.scale}"),
    on_interaction_end=lambda e: print("结束交互"),
)
```

---

## 61. Canvas 自定义绘制

**Canvas 推荐导入方式：**
```python
import flet as ft
import flet.canvas as cv

# 使用 cv 别名访问 Canvas 控件
canvas = cv.Canvas(width=400, height=300)
```

**Canvas 绘制组件：**
```python
import flet as ft
import flet.canvas as cv

# 创建 Canvas，直接在 shapes 中添加形状
canvas = cv.Canvas(
    width=400,
    height=300,
    shapes=[
        # 矩形
        cv.Rect(
            x=50, y=50, width=100, height=80,
            paint=ft.Paint(color=ft.Colors.BLUE, style=ft.PaintingStyle.FILL),
        ),
        # 圆形
        cv.Circle(
            x=100, y=200, radius=40,
            paint=ft.Paint(color=ft.Colors.RED, stroke_width=2),
        ),
        # 文字
        cv.Text(
            x=50, y=150,
            value="Canvas 文字",
            style=ft.TextStyle(size=18, color=ft.Colors.BLACK),
        ),
    ],
)

# 动态添加形状
canvas.shapes.append(
    cv.Arc(
        x=50, y=50, width=100, height=100,
        start_angle=0, sweep_angle=math.pi,
        paint=ft.Paint(stroke_width=2, style=ft.PaintingStyle.STROKE),
    )
)

# 绘制路径
path = cv.Path(
    paint=ft.Paint(stroke_width=2, style=ft.PaintingStyle.STROKE),
    elements=[
        cv.Path.MoveTo(x=0, y=0),
        cv.Path.LineTo(x=100, y=50),
        cv.Path.LineTo(x=50, y=100),
    ],
)
canvas.shapes.append(path)
```

---

## 62. ProgressRing/ProgressBar 进度控件

**进度指示器：**
```python
# 确定进度
ft.ProgressBar(value=0.7, bar_height=10, color=ft.Colors.BLUE)
ft.ProgressRing(value=0.5, width=60, height=60, color=ft.Colors.GREEN)

# 不确定进度（加载中动画）
ft.ProgressBar(value=None)  # 或不设置 value
ft.ProgressRing(value=None)
```

---

## 快速参考表

### 废弃控件替代

| 废弃控件 | 替代控件 | 说明 |
|---------|---------|------|
| `ft.ElevatedButton` | `ft.Button` | 统一使用 Button 控件 |
| `ft.border.all()` | `ft.Border.all()` | Border 类静态方法 |

### 控件属性重命名速查

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

---

## 64. Radio 必须包裹在 RadioGroup 中

**⚠️ `ft.Radio` 不能单独使用，必须包裹在 `ft.RadioGroup` 中！**

**错误写法：**
```python
# ❌ Radio 直接使用 - 报错：Radio must be enclosed within RadioGroup
ft.Radio(value="1", label="单选")

# ❌ 多个 Radio 直接放在 Row 中 - 报错
ft.Row([
    ft.Switch(label="开关"),
    ft.Checkbox(label="复选框"),
    ft.Radio(value="1", label="单选"),  # 报错！
])
```

**正确写法：**
```python
# ✅ 单个 Radio 用 RadioGroup 包裹
ft.RadioGroup(
    value="1",
    content=ft.Radio(value="1", label="单选"),
)

# ✅ 多个 Radio 在同一 Row 中
ft.Row([
    ft.Switch(label="开关"),
    ft.Checkbox(label="复选框"),
    ft.RadioGroup(
        value="1",
        content=ft.Radio(value="1", label="单选"),
    ),
])
```

---

## 65. TabBarView 高度约束要求

**⚠️ `TabBarView` 底层是 Flutter 的 `PageView`，需要从父级获得确切的高度约束！**

**错误写法：**
```python
# ❌ TabBarView 没有设置自身的 height 属性
ft.Tabs(
    content=ft.Column([
        ft.TabBar(tabs=[ft.Tab(label="标签1")]),
        ft.TabBarView(controls=[
            ft.Container(content=ft.Text("内容")),
        ]),
    ]),
    length=1,
)

# ❌ 不可靠：用 Container 包裹 Tabs + expand=True（在 scroll Column 中仍可能报错）
```

**正确写法：**
```python
# ✅ 最可靠方案：直接给 TabBarView 设置 height 属性
ft.Tabs(
    content=ft.Column([
        ft.TabBar(tabs=[ft.Tab(label="标签1")]),
        ft.TabBarView(
            height=120,  # ✅ 直接设 height！TabBarView 继承 LayoutControl
            controls=[
                ft.Container(content=ft.Text("内容")),
            ],
        ),
    ]),
    length=1,
)
```

**原理说明：**
- `TabBarView` 继承自 `LayoutControl`，拥有 `height` 和 `expand` 属性
- 在 scrollable 容器中（如 `Column(scroll=AUTO)`），子控件获得的是 unbounded height
- Flutter 的 `PageView`（TabBarView 底层实现）**必须**有明确的高度约束
- `Container` 包裹在 scrollable Column 中可能无法正确传递约束给深层嵌套的 TabBarView
- **直接给 TabBarView 设 `height` 是最可靠的方式**

---

## 66. PopupMenuItem 参数变更

**⚠️ `ft.PopupMenuItem` 的 `text` 参数已移除，必须使用 `content` 参数！**

**错误写法：**
```python
# ❌ Flet 0.x 写法 - Flet 1.0+ 报错
ft.PopupMenuButton(
    items=[
        ft.PopupMenuItem(text="个人资料"),  # 报错：unexpected keyword argument 'text'
        ft.PopupMenuItem(text="设置"),
    ],
)
```

**正确写法：**
```python
# ✅ Flet 1.0+ 写法
ft.PopupMenuButton(
    items=[
        ft.PopupMenuItem(content=ft.Text("个人资料")),  # 使用 content 参数
        ft.PopupMenuItem(content=ft.Text("设置")),
        ft.PopupMenuItem(  # 带图标的菜单项
            icon=ft.Icon(ft.Icons.SETTINGS),
            content=ft.Text("系统设置"),
        ),
        ft.PopupMenuItem(),  # 分隔线
        ft.PopupMenuItem(
            content=ft.Text("删除", color=ft.Colors.RED),
        ),
    ],
)
```

**关键变更：**
- ❌ `text` 参数已移除
- ✅ 必须使用 `content` 参数，通常传入 `ft.Text(...)`
- ✅ 支持 `icon` 参数传入 `ft.Icon(...)`
- ✅ 支持自定义 content（如 `ft.Row([ft.Icon(...), ft.Text(...)])`）

---

## 67. 快速参考表

### 废弃控件替代

| 废弃控件 | 替代控件 | 说明 |
|---------|---------|------|
| `ft.ElevatedButton` | `ft.Button` | 统一使用 Button 控件 |
| `ft.border.all()` | `ft.Border.all()` | Border 类静态方法 |

### 控件属性重命名速查

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

## 67. Window.transparent 属性移除

**变更说明**：`page.window.transparent` 属性在 Flet 1.0+ 中已被移除

**旧代码（Flet 0.x）**：
```python
# 设置透明窗口
page.window.transparent = True
page.bgcolor = ft.Colors.TRANSPARENT

# 启动参数
ft.run(main, transparent_window=True)
```

**新代码（Flet 1.0+）**：
```python
# ❌ 报错: 'Window' object has no attribute 'transparent'
# page.window.transparent = True

# 替代方案（平台可能有差异）
page.bgcolor = ft.Colors.TRANSPARENT
# 注意：transparent_window 启动参数也已失效
```

**迁移要点**：
- `page.window.transparent` 属性已完全移除
- `ft.run(transparent_window=True)` 启动参数已失效
- 透明窗口效果可能需要平台特定的替代方案

---

## 68. Dropdown on_change 改为 on_select

**变更说明**：`ft.Dropdown` 控件的 `on_change` 参数在 Flet 1.0+ 中已改为 `on_select`

**旧代码（Flet 0.x）**：
```python
ft.Dropdown(
    label="选择",
    options=[ft.DropdownOption("A"), ft.DropdownOption("B")],
    on_change=lambda e: print(e.control.value),  # ❌ 参数不存在
)
```

**新代码（Flet 1.0+）**：
```python
ft.Dropdown(
    label="选择",
    options=[ft.DropdownOption("A"), ft.DropdownOption("B")],
    on_select=lambda e: print(e.control.value),  # ✅ 正确参数名
)
```

**迁移要点**：
- `on_change` 参数已移除，改为 `on_select`
- 事件处理器签名保持不变
- 如需监听文本输入变化，使用 `on_text_change`（仅 editable=True 时）

---

## 69. ft.Audio 控件已完全移除

**变更说明**：`ft.Audio` 控件在 Flet 1.0+ (>=0.82.0) 中已**完全移除**，无官方替代方案

**旧代码（Flet 0.x）**：
```python
# ❌ 报错: module 'flet' has no attribute 'Audio'
audio = ft.Audio(
    src="audio.mp3",
    autoplay=False,
    on_loaded=lambda e: print("loaded"),
)
page.services.append(audio)  # 即使这样也无法使用
```

**替代方案**：
```python
# ✅ 使用第三方音频库
import pygame
pygame.mixer.init()
pygame.mixer.music.load("audio.mp3")
pygame.mixer.music.play()

# 或使用 pydub
from pydub import AudioSegment
from pydub.playback import play
audio = AudioSegment.from_file("audio.mp3")
play(audio)
```

**迁移要点**：
- `ft.Audio` 控件已完全移除，无替代控件
- 需使用第三方库：pygame, pydub, simpleaudio 等
- Web 应用可使用 Web Audio API

---

## 70. page.clipboard 已弃用，改用 ft.Clipboard()

**变更说明**：`page.clipboard` 在 Flet 0.80.0+ 中已弃用，将在 0.90.0 中移除，必须使用 `ft.Clipboard()` 类

**旧代码（Flet 0.x）**：
```python
# ❌ 弃用警告: clipboard is deprecated since version 0.80.0
await page.clipboard.set("文本")
content = await page.clipboard.get()
```

**新代码（Flet 1.0+）**：
```python
# ✅ 正确用法
clipboard = ft.Clipboard()
await clipboard.set("文本")
content = await clipboard.get()
```

**迁移要点**：
- 创建 `ft.Clipboard()` 实例替代 `page.clipboard`
- API 保持不变：`set(text)` 和 `get()` 仍然是异步方法
- 建议在应用启动时创建实例，多处复用

---

## 71. Window 异步方法（center/close）

**变更说明**：`page.window.center()` 和 `page.window.close()` 在 Flet 1.0+ 中都是**异步方法**，必须使用 `await` 调用

**旧代码（同步调用）**：
```python
def center_window():
    page.window.center()  # ❌ RuntimeWarning: coroutine was never awaited
    page.update()

def close_window():
    page.window.close()    # ❌ RuntimeWarning: coroutine was never awaited
```

**新代码（异步调用）**：
```python
async def center_window():
    await page.window.center()  # ✅ 正确
    page.update()

async def close_window():
    await page.window.close()   # ✅ 正确

# 在事件处理器中调用
ft.Button(
    content=ft.Text("居中"),
    on_click=lambda e: asyncio.create_task(center_window())
)
ft.Button(
    content=ft.Text("关闭"),
    on_click=lambda e: asyncio.create_task(close_window())
)
```

---

## 72. Window.max_width/max_height 可能为 None

**变更说明**：`page.window.max_width` 和 `page.window.max_height` 在某些情况下可能返回 `None`

**问题代码**：
```python
# ❌ TypeError: unsupported operand type(s) for -: 'NoneType' and 'float'
page.window.left = page.window.max_width - page.window.width
```

**解决方案**：
```python
# ✅ 使用默认值处理 None
max_w = page.window.max_width or 1920
max_h = page.window.max_height or 1080
win_w = page.window.width or 800
win_h = page.window.height or 600
page.window.left = max_w - win_w
page.window.top = max_h - win_h
```

---

## 73. Draggable on_drag_end 改为 on_drag_complete

**变更说明**：`ft.Draggable` 控件的 `on_drag_end` 参数在 Flet 1.0+ 中已改为 `on_drag_complete`

**旧代码（Flet 0.x）**：
```python
ft.Draggable(
    group="items",
    content=ft.Text("拖拽我"),
    on_drag_start=on_drag_start,
    on_drag_end=on_drag_end,  # ❌ 参数不存在
)
```

**新代码（Flet 1.0+）**：
```python
ft.Draggable(
    group="items",
    content=ft.Text("拖拽我"),
    on_drag_start=on_drag_start,
    on_drag_complete=on_drag_complete,  # ✅ 正确参数名
)
```

**迁移要点**：
- `on_drag_end` 参数已移除，改为 `on_drag_complete`
- 其他参数如 `on_drag_start` 保持不变
- 事件处理器签名不变，仍然接收 `e` 参数

---

## 74. DragUpdateEvent 属性变更

**变更说明**：`DragUpdateEvent` 的 `local_x`/`local_y` 属性在 Flet 1.0+ 中已改为 `local_position`（`Offset` 类型）

**旧代码（Flet 0.x）**：
```python
def on_pan_update(e):
    x = e.local_x  # ❌ AttributeError
    y = e.local_y  # ❌ AttributeError
```

**新代码（Flet 1.0+）**：
```python
def on_pan_update(e):
    x = e.local_position.x  # ✅ 正确
    y = e.local_position.y  # ✅ 正确
```

**相关变更**：
| 旧属性（Flet 0.x） | 新属性（Flet 1.0+） | 类型 |
|-------------------|-------------------|------|
| `e.local_x` | `e.local_position.x` | `float` |
| `e.local_y` | `e.local_position.y` | `float` |
| `e.global_x` | `e.global_position.x` | `float` |
| `e.global_y` | `e.global_position.y` | `float` |

---

## 75. PaintStyle 枚举改为 PaintingStyle

**变更说明**：Canvas 绘图用的 `ft.PaintStyle` 枚举在 Flet 1.0+ 中已改为 `ft.PaintingStyle`

**旧代码（Flet 0.x）**：
```python
paint=ft.Paint(
    color=ft.Colors.BLUE,
    style=ft.PaintStyle.STROKE,  # ❌ 属性不存在
)
```

**新代码（Flet 1.0+）**：
```python
paint=ft.Paint(
    color=ft.Colors.BLUE,
    style=ft.PaintingStyle.STROKE,  # ✅ 正确枚举名
)
```

**迁移要点**：
- `ft.PaintStyle` 已改为 `ft.PaintingStyle`
- 枚举值保持不变：`STROKE`, `FILL`

---

## 76. Paint stroke_dash 改为 stroke_dash_pattern

**变更说明**：`ft.Paint` 控件的 `stroke_dash` 参数在 Flet 1.0+ 中已改为 `stroke_dash_pattern`

**旧代码（Flet 0.x）**：
```python
paint=ft.Paint(
    color=ft.Colors.BLUE,
    stroke_dash=[10, 5],  # ❌ 参数不存在
)
```

**新代码（Flet 1.0+）**：
```python
paint=ft.Paint(
    color=ft.Colors.BLUE,
    stroke_dash_pattern=[10, 5],  # ✅ 正确参数名
)
```

**迁移要点**：
- `stroke_dash` 参数已移除，改为 `stroke_dash_pattern`
- 用法保持不变：传入虚线模式列表

---

## 77. Polygon 控件已移除，改用 Path

**变更说明**：`ft.canvas.Polygon` 控件在 Flet 1.0+ 中已移除，必须使用 `ft.canvas.Path` 绘制多边形

**旧代码（Flet 0.x）**：
```python
points = [
    ft.Point(450, 50),
    ft.Point(500, 100),
    ft.Point(480, 150),
]
canvas.shapes.append(
    ft.canvas.Polygon(  # ❌ Polygon 已移除
        points=points,
        paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
    )
)
```

**新代码（Flet 1.0+）**：
```python
canvas.shapes.append(
    ft.canvas.Path(  # ✅ 使用 Path 绘制多边形
        elements=[
            ft.canvas.Path.MoveTo(450, 50),
            ft.canvas.Path.LineTo(500, 100),
            ft.canvas.Path.LineTo(480, 150),
            ft.canvas.Path.Close(),
        ],
        paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
    )
)
```

**迁移要点**：
- `Polygon` 控件已完全移除
- 使用 `Path` + `MoveTo` + `LineTo` + `Close()` 组合绘制多边形
- 更灵活，支持复杂路径

---

## 79. BorderRadius 必须提供全部四个参数

**变更说明**：`ft.BorderRadius` 在 Flet 1.0+ 中必须提供所有四个参数，不再支持部分参数

**⚠️ 参数名警告**：参数名是 `top_left/top_right/bottom_left/bottom_right`（完整单词），**不是** `tl/tr/bl/br`（缩写）！

**旧代码（Flet 0.x）**：
```python
border_radius=ft.BorderRadius(top_left=5, top_right=5)  # ❌ 缺少 bottom_left 和 bottom_right
```

**新代码（Flet 1.0+）**：
```python
# ✅ 必须提供全部四个参数（参数名是 top_left/top_right/bottom_left/bottom_right）
border_radius=ft.BorderRadius(top_left=5, top_right=5, bottom_left=0, bottom_right=0)

# ✅ 或使用便捷函数设置统一圆角（>= 0.80.0）
border_radius=ft.BorderRadius.all(10)  # ⚠️ 使用 BorderRadius.all()（大写 B）

# ❌ 旧版本（已弃用，将在 0.83.0 移除）
border_radius=ft.border_radius.all(10)  # DeprecationWarning

# ✅ 或只设置部分圆角
border_radius=ft.border_radius.only(top_left=5, top_right=5, bottom_left=0, bottom_right=0)
```

**迁移要点**：
- `BorderRadius()` 构造函数现在需要四个必需参数
- 参数名是完整单词：`top_left`/`top_right`/`bottom_left`/`bottom_right`（不是缩写 `tl`/`tr`/`bl`/`br`）
- 如需统一圆角，使用 `ft.BorderRadius.all(value)`（大写 B，>= 0.80.0）
- 如需单独设置，使用 `ft.border_radius.only(...)` 或直接构造 `BorderRadius(...)` 并提供全部参数

---

## 80. Padding.symmetric() 弃用 → Padding.symmetric()

**影响版本**：Flet >= 0.80.0
**移除版本**：Flet 0.83.0

**错误写法（已弃用）**：
```python
# ❌ 从 0.80.0 开始弃用，将在 0.83.0 移除
padding=ft.padding.symmetric(horizontal=12, vertical=8)
```

**正确写法**：
```python
# ✅ 使用 Padding.symmetric()（注意大写 P）
padding=ft.Padding.symmetric(horizontal=12, vertical=8)

# ✅ 其他 Padding 用法不受影响
padding=ft.padding.only(left=10, top=5)  # ✅ 仍然可用
padding=10  # ✅ 简写仍然可用
```

**错误信息**：
```
DeprecationWarning: symmetric() is deprecated since version 0.80.0 
and will be removed in version 0.83.0. Use Padding.symmetric() instead
```

---

## 81. Border.all() 弃用 → Border.all()

**影响版本**：Flet >= 0.80.0
**移除版本**：Flet 0.83.0

**错误写法（已弃用）**：
```python
# ❌ 从 0.80.0 开始弃用，将在 0.83.0 移除
border=ft.border.all(2, ft.Colors.RED_300)
```

**正确写法**：
```python
# ✅ 使用 Border.all()（注意大写 B）
border=ft.Border.all(2, ft.Colors.RED_300)

# ✅ 其他 border 用法不受影响
border=ft.border.only(left=ft.BorderSide(2, ft.Colors.BLUE))  # ✅ 仍然可用
```

**错误信息**：
```
DeprecationWarning: all() is deprecated since version 0.80.0 
and will be removed in version 0.83.0. Use Border.all() instead
```

**迁移指南**：
| 旧写法 | 新写法 |
|--------|--------|
| `ft.border.all(2, color)` | `ft.Border.all(2, color)` |
| `ft.border.all(1, color)` | `ft.Border.all(1, color)` |

---

## 82. 后台线程修改控件属性导致竞态条件

**影响版本**：Flet >= 0.80.0
**严重程度**：🔴 高（导致 RuntimeError 崩溃）

**错误写法**：
```python
# ❌ 在 page.run_thread 中直接修改控件属性并调用 update()
async def loop():
    while True:
        game_stack.controls = ctrls  # 直接在后台线程修改控件属性
        game_stack.update()           # 后台线程调用 update
        await asyncio.sleep(1/60)

page.run_thread(lambda: asyncio.run(loop()))
```

**错误信息**：
```
RuntimeError: dictionary changed size during iteration
```

**根本原因**：
- `page.run_thread` 在后台线程执行
- 修改 `Stack.controls` 等控件属性时，Flet 主线程可能同时在 diff 控件树
- 导致 "dictionary changed size during iteration" 竞态条件

**正确写法**：
```python
# ✅ 使用普通函数 + time.sleep() 作为游戏循环，page.run_task() fire-and-forget
def game_loop():
    while True:
        game.update(dt)
        # UI 更新必须在主线程执行（fire-and-forget，不要 await）
        page.run_task(_update_ui)
        time.sleep(FRAME_DT)

async def _update_ui():
    """UI 更新函数，必须是 async def"""
    ft.context.disable_auto_update()
    game_stack.controls = ctrls
    game_stack.update()
    hud.update()
    ft.context.enable_auto_update()

page.run_thread(game_loop)
```

**关键规则**：
- ❌ 不能在 `page.run_thread` 中直接修改控件属性
- ❌ 不能在 `page.run_thread` 中调用 `control.update()`
- ❌ `page.run_task()` 传入的函数必须是 `async def`（不是普通 `def`）
- ❌ 不能在 `page.run_thread` 中使用 `asyncio.run()`，会导致 Future 类型冲突
- ✅ 后台游戏循环用普通 `def` + `time.sleep()`，不用 asyncio
- ✅ `page.run_task(_update_ui)` 是 fire-and-forget 模式，不要 await
- ✅ 游戏逻辑（位置计算、碰撞检测）可以在后台线程执行
- ✅ 只有实际修改 Flet 控件属性的操作需要通过 `page.run_task()` 调度

---

**文档版本**：Flet >= 0.82.0
**破坏性变更数量**：82项
**最后更新**：2026年3月
