# Android Finance Spec

> Stop shipping `Double` for money. Stop breaking Arabic layouts. Let AI catch these before they hit production.

**English** | [简体中文](./README.zh-CN.md)

![Skills](https://img.shields.io/badge/skills-1-blue) ![Platform](https://img.shields.io/badge/platform-Android%20%7C%20Kotlin-green) ![License](https://img.shields.io/badge/license-MIT-black) ![Agents](https://img.shields.io/badge/agents-Codex%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Copilot-purple)

![Android Finance Spec](./share/android-finance-skill-card.png)

## The Problem

Android finance apps silently lose money — literally. `Double` truncates crypto decimals. `left`/`right` layouts flip Arabic text. Hardcoded strings bypass translation pipelines. These bugs are invisible in code review but catastrophic in production.

**This skill teaches your AI coding agent to catch them all — at write time, not deploy time.**

## Scanner Demo

Run the bundled scanner on any Android project to get instant findings:

```bash
python3 skills/android-finance-spec/scripts/android_finance_scan.py /path/to/your-android-project
```

**Before** — 18 issues found in a typical finance DTO:

```text
## [P1] FIN_FLOATING_DECIMAL_FIELD
- Snippet: `val amount: Double?,`

## [P1] RTL_LEFT_RIGHT_XML
- Snippet: `android:layout_marginLeft="16dp"`

## [P1] I18N_HARDCODED_ANDROID_TEXT
- Snippet: `android:text="Price +5.23%"`
```

**After** — zero issues:

```text
# Android Finance Spec Scan
No first-pass issues found.
```

## Quick Start

```bash
npx skills add brycegao/android-finance-spec --path skills/android-finance-spec
```

Then use the slash command in your agent terminal:

```text
/android-finance-spec    # Review current changes
```

Or invoke from chat:

```text
Use $android-finance-spec to review this Android Kotlin change.
```

## What It Catches

| Category | Rules |
|----------|-------|
| **Financial Precision** | `Double`/`Float` fields, unsafe `BigDecimal` constructors, `.toDouble()` conversions, `toString()` → scientific notation |
| **RTL / i18n** | `left`/`right` layout attributes, hardcoded `layoutDirection`, missing `keepLTR()`, hardcoded visible text, missing `textDirection="ltr"` |
| **Kotlin Safety** | `!!` assertions, `GlobalScope`, naked `launch` without error handling |

## Specs

| Spec | Focus |
|------|-------|
| [**Financial Precision**](./specs/finance-number-skill.md) | `String?`/`BigDecimal` DTOs, `NumericFormat` display, Gson config, boundary fallback to `null`/`--` |
| [**RTL & i18n**](./specs/rtl-adaption.md) | `start`/`end` layouts, `keepLTR()` isolation, `{0}/{1}` placeholders, TextView mandatory attributes |
| [**Kotlin Style**](./specs/kotlin-style.md) | Project-first architecture, MVI/MVVM, coroutine/Flow safety, null-safety, no reinvented helpers |

## Agent Integration

Add one line to your project's agent config to activate all specs:

| Agent | Config File | Content |
|-------|-------------|---------|
| **Claude Code** | `CLAUDE.md` | `Before generating code, read specs/finance-number-skill.md, specs/rtl-adaption.md, specs/kotlin-style.md. All MUST/MUST NOT rules are mandatory.` |
| **Cursor** | `.cursor/rules/android-finance.mdc` | Same three spec paths + `globs: ["**/*.kt", "**/*.xml"]` + `alwaysApply: true` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Same three spec paths + project-first directive |
| **Codex** | `AGENTS.md` | Same three spec paths + hard gate rules |

<details>
<summary>📋 Full config templates</summary>

### Claude Code — `CLAUDE.md`

```md
This is an Android Kotlin finance app.

Before code generation, refactoring, or review, read:

1. specs/finance-number-skill.md
2. specs/rtl-adaption.md
3. specs/kotlin-style.md

All MUST and MUST NOT rules are mandatory.
If a spec conflicts with existing project implementation, follow the project.
```

### Cursor — `.cursor/rules/android-finance.mdc`

```md
---
description: Android finance precision, RTL/i18n, and Kotlin style
globs:
  - "**/*.kt"
  - "**/*.xml"
alwaysApply: true
---

This project must follow:
- @specs/finance-number-skill.md
- @specs/rtl-adaption.md
- @specs/kotlin-style.md

Enforce every MUST and MUST NOT rule.
Search for existing patterns before adding new code.
```

### GitHub Copilot — `.github/copilot-instructions.md`

```md
When generating or editing Kotlin/Android code, follow:
- specs/finance-number-skill.md
- specs/rtl-adaption.md
- specs/kotlin-style.md

Prefer existing project architecture. Do not reinvent existing helpers.
```

### Codex — `AGENTS.md`

```md
You are a senior Android + Kotlin engineer. Follow:
- specs/finance-number-skill.md
- specs/rtl-adaption.md
- specs/kotlin-style.md

MUST/MUST NOT rules are hard gates. Do not invent missing base classes.
```

</details>

## Recommended Project Layout

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
