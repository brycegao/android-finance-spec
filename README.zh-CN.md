# Android Finance Spec

> 别再用 `Double` 存钱了，别再让阿拉伯语布局错位了。让 AI 在写代码时就拦住这些问题。

[English](./README.md) | **简体中文**

![Skills](https://img.shields.io/badge/skills-1-blue) ![Platform](https://img.shields.io/badge/platform-Android%20%7C%20Kotlin-green) ![License](https://img.shields.io/badge/license-MIT-black) ![Agents](https://img.shields.io/badge/agents-Codex%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Copilot-purple)

![Android Finance Spec](./share/android-finance-skill-card.png)

## 问题在哪

Android 金融 App 在悄悄亏钱 — 字面意义上的。`Double` 截断加密小数位，`left`/`right` 布局翻转阿拉伯语文本，硬编码字符串绕过翻译管线。这些问题在 Code Review 中几乎看不见，但上线后代价惨重。

**这个技能让你的 AI 编码代理在写代码时就捕获它们 — 不是部署时。**

## 扫描器演示

对任意 Android 项目运行内置扫描器，即时获得检查结果：

```bash
python3 skills/android-finance-spec/scripts/android_finance_scan.py /path/to/your-android-project
```

**修复前** — 典型金融 DTO 发现 18 个问题：

```text
## [P1] FIN_FLOATING_DECIMAL_FIELD
- Snippet: `val amount: Double?,`

## [P1] RTL_LEFT_RIGHT_XML
- Snippet: `android:layout_marginLeft="16dp"`

## [P1] I18N_HARDCODED_ANDROID_TEXT
- Snippet: `android:text="Price +5.23%"`
```

**修复后** — 零问题：

```text
# Android Finance Spec Scan
No first-pass issues found.
```

## 快速开始

```bash
npx skills add brycegao/android-finance-spec --path skills/android-finance-spec
```

在 Agent 终端中使用 slash 命令：

```text
/android-finance-spec    # 审查当前改动
```

也可以在对话中直接调用：

```text
Use $android-finance-spec to review this Android Kotlin change.
```

## 检查内容

| 分类 | 规则 |
|------|------|
| **金融精度** | `Double`/`Float` 字段、不安全的 `BigDecimal` 构造、`.toDouble()` 转换、`toString()` 导致科学计数法 |
| **RTL / 国际化** | `left`/`right` 布局属性、硬编码 `layoutDirection`、缺失 `keepLTR()`、硬编码可见文案、缺失 `textDirection="ltr"` |
| **Kotlin 安全** | `!!` 断言、`GlobalScope`、无异常处理的裸 `launch` |

## 规范文档

| 规范 | 聚焦 |
|------|------|
| [**金融精度**](./specs/finance-number-skill.md) | `String?`/`BigDecimal` DTO、`NumericFormat` 展示、Gson 配置、边界兜底返回 `null`/`--` |
| [**RTL & 国际化**](./specs/rtl-adaption.md) | `start`/`end` 布局、`keepLTR()` 隔离、`{0}/{1}` 占位符、TextView 必填属性 |
| [**Kotlin 风格**](./specs/kotlin-style.md) | 项目优先架构、MVI/MVVM、协程/Flow 安全、空安全、禁止重复造轮子 |

## Agent 接入

在项目的 Agent 配置中添加一行即可激活全部规范：

| Agent | 配置文件 | 内容 |
|-------|---------|------|
| **Claude Code** | `CLAUDE.md` | 生成代码前读取 specs/finance-number-skill.md、specs/rtl-adaption.md、specs/kotlin-style.md，所有 MUST/MUST NOT 规则强制执行 |
| **Cursor** | `.cursor/rules/android-finance.mdc` | 同上三个 spec 路径 + `globs: ["**/*.kt", "**/*.xml"]` + `alwaysApply: true` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | 同上三个 spec 路径 + 项目优先指令 |
| **Codex** | `AGENTS.md` | 同上三个 spec 路径 + 强制门禁规则 |

<details>
<summary>📋 完整配置模板</summary>

### Claude Code — `CLAUDE.md`

```md
本项目是 Android Kotlin 金融类 App。

每次进行代码生成、重构、Review 前，必须先读取：

1. specs/finance-number-skill.md
2. specs/rtl-adaption.md
3. specs/kotlin-style.md

所有 MUST / MUST NOT 规则视为强制约束。
如通用规范与项目已有实现或工具配置冲突，以项目已有实现和工具配置为准。
```

### Cursor — `.cursor/rules/android-finance.mdc`

```md
---
description: Android 金融数值、RTL 国际化与 Kotlin 风格强制规范
globs:
  - "**/*.kt"
  - "**/*.xml"
alwaysApply: true
---

本项目必须遵守：
- @specs/finance-number-skill.md
- @specs/rtl-adaption.md
- @specs/kotlin-style.md

生成、修改、Review Android 代码时，必须执行 specs 中的 MUST / MUST NOT 规则。
新增代码前必须先检索项目已有实现，优先复用项目现有架构、封装和工具配置。
```

### GitHub Copilot — `.github/copilot-instructions.md`

```md
生成或修改 Kotlin / Android 代码时，必须遵循项目统一代码规范：
- specs/finance-number-skill.md
- specs/rtl-adaption.md
- specs/kotlin-style.md

优先遵循项目已有架构，不要重复造已有工具。
```

### Codex — `AGENTS.md`

```md
你是资深 Android + Kotlin 工程师，当前项目必须遵守：
- specs/finance-number-skill.md
- specs/rtl-adaption.md
- specs/kotlin-style.md

所有 MUST / MUST NOT 规则都是强制门禁。不要臆造项目中不存在的基类。
```

</details>

## 推荐目录结构

```text
your-android-project/
  AGENTS.md
  CLAUDE.md
  .cursor/rules/android-finance.mdc
  .github/copilot-instructions.md
  specs/
    finance-number-skill.md
    rtl-adaption.md
    kotlin-style.md
```

## License

[MIT](./LICENSE) © 2026 Bryce
