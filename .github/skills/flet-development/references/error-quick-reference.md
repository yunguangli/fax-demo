# Flet 1.0+ 错误快速参考

> 本文档提供常见错误的快速定位和解决方案。
> 
> **详细说明**：见 [error-guide.md](error-guide.md)

---

## 高频错误（按出现频率排序）

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `unexpected keyword argument 'tabs'` | Tabs API 完全重写 | 用 `Tabs(content=..., length=N)` + `TabBar` + `TabBarView` |
| `unexpected keyword argument 'tl'` | BorderRadius 参数名错误 | 用 `top_left/top_right/bottom_left/bottom_right`（完整单词）|
| `missing required argument 'content'` | Tabs 缺少参数 | Tabs 需要 `content` 和 `length` 参数 |
| `unexpected keyword argument 'content'` | Tab 没有 `content` 参数 | `ft.Tab(label=..., icon=...)` |
| `unexpected keyword argument 'label_style'` | Badge 只能用 `label` 参数 | `ft.Badge(label="5")` |
| `unexpected keyword argument 'small'` | Badge 只能用 `label` 参数 | `ft.Badge(label="5")` |
| `Radio must be enclosed within RadioGroup` | Radio 没有被 RadioGroup 包裹 | `ft.RadioGroup(content=ft.Radio(...))` |
| `height is unbounded` | TabBarView 没设置 height | **直接给 `TabBarView` 设 `height=固定值`** |
| `'super' object has no attribute '__getattr__'` | 使用了 `ft.Colors.values()` | 手动定义颜色列表 |
| `unexpected keyword argument 'text'` | TextButton 不支持 text 参数 | 用 `content` 参数或直接传字符串 |
| `unexpected keyword argument 'name'` | Icon 不支持 `name` 参数 | 用 `icon=` 参数 |
| `ElevatedButton is not defined` | ElevatedButton 已移除 | 用 `ft.Button()` 或 `ft.FilledButton()` |
| `'NavigationDrawer' object has no attribute 'open'` | drawer 使用方式变更 | 用 `await page.show_drawer()` / `close_drawer()` |
| `'Window' object has no attribute 'transparent'` | transparent 属性已移除 | 该属性已完全移除 |
| `coroutine 'Window.center' was never awaited` | `window.center()` 是异步方法 | 用 `await page.window.center()` |
| `coroutine 'Window.close' was never awaited` | `window.close()` 是异步方法 | 用 `await page.window.close()` |
| `clipboard is deprecated` | `page.clipboard` 已弃用 | 用 `clipboard = ft.Clipboard()` |
| `module 'flet' has no attribute 'Audio'` | ft.Audio 控件已移除 | 用第三方库 |
| `unexpected keyword argument 'on_change'` | Dropdown 参数名变更 | 用 `on_select` |
| `module 'flet' has no attribute 'PaintStyle'` | 枚举名变更 | 用 `ft.PaintingStyle` |
| `module 'flet.canvas' has no attribute 'Polygon'` | Polygon 控件已移除 | 用 `ft.canvas.Path` |
| `unexpected keyword argument 'stroke_dash'` | 参数名变更 | 用 `stroke_dash_pattern` |
| `'Path' object has no attribute 'move_to'` | Path 构建方式变更 | 用 `elements=[Path.MoveTo(...)]` |
| `missing 2 required positional arguments` | BorderRadius 缺少参数 | 必须提供全部四个参数 |
| `unexpected keyword argument 'on_drag_end'` | 参数名变更 | 用 `on_drag_complete` |
| `'DragUpdateEvent' object has no attribute 'local_x'` | 属性名变更 | 用 `e.local_position.x` |
| `TypeError: unsupported operand type(s) for -: 'NoneType'` | `max_width/max_height` 可能为 None | 用 `page.window.max_width or 1920` |
| `AttributeError: ROBOT` | Icons.ROBOT 不存在 | 用 `ft.Icons.ANDROID` |
| `AttributeError: 'Page' object has no attribute 'open'` | page.open() 不存在 | 用 `page.show_dialog()` |
| `AttributeError: 'Page' object has no attribute 'close'` | page.close() 不存在 | 用 `page.pop_dialog()` |
| `DeprecationWarning: symmetric() is deprecated` | `ft.padding.symmetric()` 已弃用 | 用 `ft.Padding.symmetric()`（大写 P） |
| `DeprecationWarning: all() is deprecated ... Use Border.all` | `ft.border.all()` 已弃用 | 用 `ft.Border.all()`（大写 B） |
| `RuntimeError: dictionary changed size during iteration` | 后台线程直接修改控件属性 | 用 `await page.run_task()` 在主线程执行 UI 更新 |
| `TypeError: handler must be a coroutine function` | `page.run_task()` 传入普通 `def` | 传入的必须是 `async def` |

---

## 快速诊断

### 报错关键词 → 可能原因

| 报错关键词 | 可能原因 |
|-----------|---------|
| `unexpected keyword argument` | 参数名已变更或移除 |
| `missing required argument` | 缺少必需参数 |
| `has no attribute` | 属性已移除或重命名 |
| `coroutine was never awaited` | 异步方法未使用 await |
| `must be a coroutine function` | 需要 `async def` |
| `height is unbounded` | TabBarView 需要设置 height |
| `is not defined` | 控件已移除或重命名 |
| `AttributeError: XXX` | 属性不存在，需检查正确名称 |

---

## 常见场景解决方案

### 1. Tabs 相关错误

**错误**：`unexpected keyword argument 'tabs'`

**原因**：Tabs API 完全重写

**解决方案**：
```python
# ❌ 旧 API
ft.Tabs(tabs=[ft.Tab(label="A")])

# ✅ 新 API - 三件套
ft.Tabs(
    content=ft.Column([
        ft.TabBar(tabs=[ft.Tab(label="标签1")]),
        ft.TabBarView(height=120, controls=[ft.Container(...)]),
    ]),
    length=1,
)
```

---

### 2. BorderRadius 相关错误

**错误**：`unexpected keyword argument 'tl'`

**原因**：参数名是完整单词，不是缩写

**解决方案**：
```python
# ❌ 错误
ft.BorderRadius(tl=5, tr=5, bl=0, br=0)

# ✅ 正确
ft.BorderRadius(top_left=5, top_right=5, bottom_left=0, bottom_right=0)

# ✅ 便捷方法（新版本，>= 0.80.0）
ft.BorderRadius.all(10)  # ⚠️ 使用 BorderRadius.all()（大写 B）

# ❌ 便捷方法（已弃用，将在 0.83.0 移除）
ft.border_radius.all(10)  # DeprecationWarning
```

---

### 3. TabBarView 高度错误

**错误**：`height is unbounded`

**原因**：TabBarView 必须设置固定高度

**解决方案**：
```python
# ❌ 错误
ft.TabBarView(controls=[...])

# ✅ 正确
ft.TabBarView(height=120, controls=[...])
```

---

### 4. Icon 相关错误

**错误**：`unexpected keyword argument 'name'`

**原因**：Icon 使用 `icon=` 参数，不是 `name=`

**解决方案**：
```python
# ❌ 错误
ft.Icon(name=ft.Icons.HOME)

# ✅ 正确
ft.Icon(icon=ft.Icons.HOME, size=24, color=ft.Colors.BLUE)
```

**错误**：`AttributeError: ROBOT`

**原因**：Icons.ROBOT 不存在

**解决方案**：
```python
# ❌ 错误
ft.Icon(ft.Icons.ROBOT)

# ✅ 正确
ft.Icon(ft.Icons.ANDROID)  # 使用 ANDROID 图标
```

---

### 5. 对话框相关错误

**错误**：`'Page' object has no attribute 'open'`

**原因**：page.open() 不存在，应使用 show_dialog()

**解决方案**：
```python
# ❌ 错误
page.open(dialog)

# ✅ 正确
page.show_dialog(dialog)
page.pop_dialog()  # 关闭
```

---

### 6. SnackBar / BottomSheet 错误

**错误**：`'Page' object has no attribute 'snack_bar'`

**原因**：page.snack_bar 已废弃

**解决方案**：
```python
# ❌ 错误
page.snack_bar = snackbar

# ✅ 正确
page.overlay.append(snackbar)
snackbar.open = True
page.update()
```

---

## 验证方法

**遇到不确定的 API，立即验证：**

```python
# 验证构造函数签名
python -c "import inspect; import flet as ft; print(inspect.signature(ft.BorderRadius.__init__))"

# 检查属性是否存在
python -c "import flet as ft; print('exists' if hasattr(ft.Icons, 'ROBOT') else 'not exists')"

# 检查所有方法
python -c "import flet as ft; print([m for m in dir(ft.Page) if not m.startswith('_')])"
```

---

**详细错误说明**：见 [error-guide.md](error-guide.md)  
**API 正确用法**：见 [api-quick-reference.md](api-quick-reference.md)  
**新发现记录**：见 [discovery-log.md](discovery-log.md)
