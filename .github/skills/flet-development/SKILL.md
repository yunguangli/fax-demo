---
name: flet-development
description: This skill should be used when developing desktop/web applications with Flet; encountering Flet 1.0+ version compatibility issues; migrating from Flet 0.x to 1.0+; encountering API errors with Tabs/Badge/Radio/BorderRadius controls; needing guidance on Flet animations, async operations, or layouts. Covers Flet 0.82.0+ with breaking changes, new controls, and best practices.
version: 1.0.1
disable: false
---

# Flet 1.0+ 开发指南

Provide expert guidance for developing Flet applications with version 1.0+ (>= 0.82.0), which introduces breaking changes from Flet 0.x and requires updated APIs, patterns, and best practices.

---

## ⚠️ CRITICAL: Before You Start

**创建新项目时，第一件事必须是：**

### ✅ 项目创建决策树

```
需要创建新的 Flet 项目？
    ↓
【是否已有项目目录和文件？】
    ├─ 否 → 使用官方脚手架，运行 flet create
    └─ 是 → 直接在用户已经预先准备好的目录和代码文件里开始编写代码。一般默认优先查找改动已有的main.py。
    ↓
【如果是flet create情况，检查生成的文件】
    ├─ pyproject.toml ✅
    ├─ src/main.py ✅
    └─ src/assets/ ✅
    ↓
【开始在 src/main.py 中编写代码】
```

### 🚨 常见错误

| 错误行为 | 后果 | 正确做法 |
|---------|------|---------|
| 直接写代码，不运行 `flet create` | 缺少标准结构、依赖管理 | **第一步**：`flet create` |
| 手动创建 pyproject.toml | 版本不兼容、配置错误 | 使用官方脚手架 |
| 在根目录直接创建 main.py | 不符合标准项目结构 | 在 `src/main.py` 编写 |

### ⚡ 快速开始命令

```bash
# 创建新项目（推荐）
flet create

# 运行项目
flet run
```

**⚠️ 重要**：`flet create` 会替换现有的 README.md 或 pyproject.toml（如果存在）；如果用户要指定项目名称，则原则上禁止项目名称包含大写字母和中文，因为可能会影响后续的项目打包。

---

## When to Use

### ✅ Invoke this skill when:

| 触发场景 | 第一行动 | 说明 |
|---------|---------|------|
| **🎨 创建新的 Flet 项目** | ⚡ **立即运行 `flet create`** | 生成标准项目结构（pyproject.toml、src/main.py 等） |
| **🔧 开发任何 Flet 功能** | ⚡ **查阅示例代码和 API 参考** | ⚠️ 必须持续查阅，不是只查一次！ |
| **🖥️ 开发桌面/Web 应用** | 加载本 skill | 获取最新 API 指导和最佳实践 |
| **🔄 从 Flet 0.x 迁移** | 查阅 Breaking Changes | 处理 79+ 个 API 变更 |
| **🐛 遇到 API 错误** | 检查 Critical API Traps | BorderRadius、Tabs、Colors、KeyboardEvent 等常见陷阱 |
| **⚙️ 异步操作** | 参考 Procedural Rules | 文件选择器、对话框、延迟 |
| **🎨 主题和样式** | 查阅 API Quick Reference | Colors、Alignment、Buttons 等 |

### ❌ Do NOT invoke for:

- General Python questions unrelated to Flet
- Flet 0.x compatibility questions (use migration guidance instead)

---

## Purpose

Flet 1.0+ introduces 79+ breaking changes from Flet 0.x, with all deprecated APIs removed. This skill provides:

1. **Accurate API usage** - Verified through Python inspect, not documentation alone
2. **Critical trap avoidance** - Common mistakes with BorderRadius, Tabs, Colors, Alignment
3. **Migration guidance** - Step-by-step migration from Flet 0.x
4. **Performance patterns** - Auto-update mechanism, batch operations

---

## Project Initialization

### Standard Project (Recommended)

To create a new Flet application from scratch:

```bash
flet create
```

This generates standard project structure:
- `pyproject.toml` - Dependency management
- `src/main.py` - Application entry point
- `src/assets/` - Static resources
- `storage/` - Data and temp directories

**Note:** Replaces existing `README.md` or `pyproject.toml` if present.

### Single-File Project

For quick prototypes or examples, create a single `.py` file:

```python
import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("Hello, Flet!"))

ft.run(main)
```

---

## Auto-Update Mechanism

Flet 1.0+ automatically calls `page.update()` at the end of event handlers and `main()` function in most cases.

### Default Behavior

```python
import flet as ft

def main(page: ft.Page):
    def button_click(e):
        page.controls.append(ft.Text("Clicked!"))
        # ✅ No need to call page.update() - auto-update enabled
    
    page.add(ft.Button("Click me", on_click=button_click))

ft.run(main)
```

### Batch Operations (Optimization)

To optimize performance when adding many controls:

```python
def add_many_items(e):
    ft.context.disable_auto_update()  # Disable auto-update
    for i in range(100):
        page.controls.append(ft.Text(f"Item {i}"))
    page.update()  # Single update instead of 100

page.add(ft.Button("Add items", on_click=add_many_items))
```

### Global Control

```python
import flet as ft

ft.context.disable_auto_update()  # Global disable

def main(page: ft.Page):
    page.add(ft.Text("Hello"))
    page.update()  # ⚠️ Must call explicitly

ft.run(main)
```

**Best Practice:** Keep auto-update enabled; disable only for performance-sensitive batch operations.

---

## Core Workflow

### ⚠️ CRITICAL: 持续查阅 Skill（必须遵守）

**⚠️ 重要教训（2026-03-20）：**
> 只在开始时查阅 skill，后续写代码时忘记查阅，导致使用了错误的 API（`KeyboardEvent.event_type` 不存在）。
> **必须持续查阅 skill 中的说明和示例代码！**

**强制工作流程：**

```
开发 Flet 功能时的强制流程：
    ↓
【第一步：查阅 Skill】
    ├─ 查看 API Quick Reference
    ├─ 查看相关示例代码
    └─ 检查破坏性变更列表
    ↓
【第二步：参考示例代码】
    ├─ examples/ 目录中的 20 个示例
    └─ 必须直接复制示例代码的结构
    ↓
【第三步：实现功能】
    ├─ 基于示例代码修改
    └─ 不确定的 API 必须验证
    ↓
【第四步：遇到问题时】
    ├─ 立即查阅 error-quick-reference.md
    └─ 查看相关示例代码的用法
```

**禁止行为：**
- ❌ 只在开始查阅一次 skill，后续凭记忆写代码
- ❌ 不参考 skill 中的示例代码
- ❌ 凭经验猜测 API 用法
- ❌ 不检查破坏性变更列表

**正确行为：**
- ✅ 每个功能开发前都查阅 skill
- ✅ 使用任何 API 前先查找示例代码
- ✅ 不确定时使用 inspect 验证
- ✅ 遇到错误立即查阅 skill 中的错误指南

### ⚡ Before Development (强制检查)

**开发前必做检查清单：**

```
1. 【项目结构检查】
   ├─ 是否有 pyproject.toml？
   ├─ 是否有 src/main.py？
   └─ 没有？→ 运行 flet create ⚠️

2. 【API 参考检查】
   └─ 查阅 [API Quick Reference](references/api-quick-reference.md)

3. 【示例代码检查】⚠️ 必须步骤
   └─ 查阅 examples/ 目录中的相关示例

4. 【不确定的 API？】
   └─ 使用 inspect 验证（见下方验证方法）
```

### Before Development

1. **Check API Quick Reference**: [references/api-quick-reference.md](references/api-quick-reference.md) - High-frequency API usage
2. **Review example code**: [examples/](examples/) - 20 complete examples **⚠️ 必须步骤**
3. **Verify uncertain APIs with inspect** (see verification method below)

### When Errors Occur

1. **Quick diagnosis**: Check [references/error-quick-reference.md](references/error-quick-reference.md)
2. **Detailed troubleshooting**: Consult [references/error-guide.md](references/error-guide.md)

### API Verification (Mandatory)

**When uncertain about an API, verify with inspect - do not rely on documentation alone!**

```python
# Verify control constructor
python -c "import inspect; import flet as ft; print(inspect.signature(ft.BorderRadius.__init__))"

# Check if control exists
python -c "import flet as ft; print('exists' if hasattr(ft, 'CircleAvatar') else 'not exists')"

# List all methods
python -c "import flet as ft; print([m for m in dir(ft.Page) if not m.startswith('_')])"
```

---

## Critical API Traps

**Most error-prone APIs (always verify):**

| API | Common Mistake | Correct Usage |
|-----|---------------|---------------|
| **Threading UI** | Use `asyncio.run()` + `await page.run_task()` | Use plain `def` + `time.sleep()` + `page.run_task()` (fire-and-forget) |
| **Border.all()** | Use `ft.border.all()` | Use `ft.Border.all()` (uppercase B, >=0.80.0) |
| **Padding.symmetric()** | Use `ft.padding.symmetric()` | Use `ft.Padding.symmetric()` (uppercase P, >=0.80.0) |
| **KeyboardEvent** | Use `page.on_key_down` / `page.on_key_up` | Use `page.on_keyboard_event` only (no separate down/up events) |
| **KeyboardEvent** | Use `e.event_type` or `e.type` to distinguish keydown/keyup | ❌ No `event_type` or `type` attribute! Events repeat while key is pressed |
| **BorderRadius** | Use `ft.border_radius.all()` | Use `ft.BorderRadius.all()` (uppercase B, >=0.80.0) |
| **Colors** | Use `DARK_RED`, `DARK_BLUE` etc. | Use Material Design: `RED_900`, `BLUE_900` |
| **Tabs** | Use `tabs=[]` parameter | Use three-part pattern: `Tabs(content=..., length=N) + TabBar + TabBarView` |
| **TabBarView** | Omit `height` parameter | Must set `height` parameter to avoid `height is unbounded` error |
| **Icon** | Use `name=` parameter | Use `icon=` parameter |
| **Badge** | Use `label_style` or `small` | Only use `label=` parameter |
| **Radio** | Use standalone | Must wrap in `RadioGroup` |
| **App Launch** | Use `ft.app(target=main)` | Use `ft.run(main)` |
| **Colors** | Use `ft.colors` (lowercase s) | Use `ft.Colors` (uppercase C) |
| **Alignment** | Use `ft.alignment.center` | Use `ft.Alignment.CENTER` (uppercase A) |
| **Buttons** | Use `ft.ElevatedButton` or `text=` parameter | Use `ft.Button(content=...)` or `ft.FilledButton(content=...)` |
| **Text** | Use `ft.Text(text=)` | Use `ft.Text(content=...)` |
| **session** | Use `page.session.get()` | Use `page.session.store.get()`|
| **session** | Use `page.session.set()` | Use `page.session.store.set()`|
| **session** | Use `page.session.clear()` | Use `page.session.store.clear()`|
| **Icons** | Use `ft.Icons.WINDOWS` | Use `ft.Icons.WINDOW`|

**Complete trap list**: See [references/api-quick-reference.md](references/api-quick-reference.md)

---

## Procedural Rules

### Application Launch

```python
# ✅ Flet 1.0+
ft.run(main)

# ❌ Flet 0.x (deprecated)
ft.app(target=main)
```

### Alignment

```python
# ✅ Flet 1.0+
ft.Alignment.CENTER
ft.Alignment.TOP_LEFT

# ❌ Flet 0.x (deprecated)
ft.alignment.center
```

### Event Handlers

```python
# ✅ Async API calls require async def
async def on_click(e):
    await file_picker.pick_files()

# ✅ Delays require asyncio.sleep
async def on_click(e):
    await asyncio.sleep(0.5)
```

### Service Controls

```python
# ✅ Register service controls explicitly
file_picker = ft.FilePicker()
page.services.append(file_picker)
```

### Dialogs

```python
# ✅ Display dialog
page.show_dialog(dialog)

# ✅ Close dialog
page.pop_dialog()

# ❌ page.open() does not exist
```

### SnackBar / BottomSheet

```python
# ✅ Correct usage
page.overlay.append(snackbar)
snackbar.open = True
page.update()

# ❌ page.snack_bar / page.bottom_sheet deprecated
```

---

## Development Checklist

### 🚨 Before Creating/Writing Code

- [ ] **【最重要】是否已运行 `flet create`？**（新项目必须先运行此命令）
- [ ] 检查 pyproject.toml 和 src/main.py 是否存在
- [ ] Use `ft.run(main)` to launch
- [ ] Use `ft.Colors.XXX` (uppercase C)
- [ ] Use `ft.Alignment.CENTER` (uppercase A)
- [ ] Use `icon=` parameter for Icon (not `name=`)
- [ ] BorderRadius parameters: `top_left/top_right/bottom_left/bottom_right` (not `tl/tr/bl/br`)
- [ ] Set `height` for TabBarView
- [ ] Verify uncertain APIs with `inspect`

### When Errors Occur

- [ ] Check if deprecated API is called
- [ ] Verify actual API signature with `inspect`
- [ ] Ensure async methods use `await` and `async def`
- [ ] Confirm service controls added to `page.services`

---

## Resources

### Reference Documentation (Load as needed)

- **[API Quick Reference](references/api-quick-reference.md)** - High-frequency API usage (recommended first)
- **[Breaking Changes Guide](references/breaking-changes.md)** - Complete list of 79 changes
- **[Error Troubleshooting Guide](references/error-guide.md)** - Detailed error solutions
- **[Discovery Log](references/discovery-log.md)** - Continuously updated findings

### Example Code (Reference as needed)

- `examples/01_basic_app.py` - Basic structure
- `examples/03_form_validation.py` - Form validation
- `examples/07_dialog_example.py` - Dialogs
- `examples/09_theme_styling.py` - Tabs three-part pattern
- Complete index: [examples/README.md](examples/README.md)

### New Discoveries

**Latest findings (2026-03-20):**
- BorderRadius parameter names are full words (not abbreviations)
- `ft.Icons.ROBOT` does not exist, use `ft.Icons.ANDROID` instead
- `ft.CircleAvatar` exists and is usable
- Dialog API: `page.show_dialog()` / `page.pop_dialog()`

Track ongoing discoveries in [references/discovery-log.md](references/discovery-log.md).

---

**Applicable Version**: Flet >= 0.82.0  
**Breaking Changes**: 82+ (continuously updated)  
**Last Updated**: 2026-03-21
