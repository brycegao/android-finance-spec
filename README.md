# Android Finance Spec Skills
> The missing AI coding standard for Android finance apps: precision-safe numbers, RTL/i18n UI, and project-first Kotlin style.

**Languages:** English | [简体中文](./README.zh-CN.md)

![Skills](https://img.shields.io/badge/skills-1-blue)
![Platform](https://img.shields.io/badge/platform-Android%20%7C%20Kotlin-green)
![License](https://img.shields.io/badge/license-MIT-black)
![Agents](https://img.shields.io/badge/agents-Codex%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Copilot-purple)

![Android Finance Spec Skill](./share/android-finance-skill-card.png)

## Skills

| Skill | Description | Install |
|-------|-------------|---------|
| [**Android Finance Spec**](./skills/android-finance-spec/) | Review and generate Android Kotlin finance code with BigDecimal/String precision, RTL/i18n safety, and project-first Kotlin style | `npx skills add brycegao/android-finance-spec --path skills/android-finance-spec` |

## Quick Start

Install any skill with:

```bash
npx skills add brycegao/android-finance-spec --path skills/<skill-name>
```

`npx` runs the npm `skills` CLI. The CLI resolves `owner/repo` from GitHub, then installs the skill folder specified by `--path`.

Install this skill:

```bash
npx skills add brycegao/android-finance-spec --path skills/android-finance-spec
```

Then invoke it in your agent terminal:

```bash
/android-finance-spec    # Review current Android Kotlin changes
```

Slash invocation depends on your agent terminal and `skills` CLI integration. If slash commands are not available, use the chat invocation below.

Or invoke it from chat:

```text
Use $android-finance-spec to review this Android Kotlin change for finance precision, RTL/i18n, and project style risks.
```

## What It Catches

- Financial decimal fields using `Double` / `Float`
- Unsafe `BigDecimal` construction and `.toDouble()` / `.toFloat()` conversions
- Handwritten financial formatting instead of a unified formatter
- RTL layout issues from `left` / `right` attributes
- Mixed RTL text risks around `+/-`, `%`, currency pairs, dates, ranges, and units
- Hardcoded visible text in Android XML
- Kotlin anti-patterns such as `!!`, `GlobalScope`, and reinvented project helpers

## Local Scanner

Run a first-pass static scan:

```bash
python3 skills/android-finance-spec/scripts/android_finance_scan.py /path/to/your-android-project
```

The scanner is intentionally conservative. Treat it as the first gate, then review findings in business context.

Try the included examples:

```bash
python3 skills/android-finance-spec/scripts/android_finance_scan.py examples/bad-android-finance
python3 skills/android-finance-spec/scripts/android_finance_scan.py examples/fixed-android-finance
```

The bad example should report finance precision, RTL layout, hardcoded text, and Kotlin coroutine/null-safety issues. The fixed example should pass.

## Verification

Run scanner regression tests:

```bash
python3 -m unittest tests/test_android_finance_scan.py
```

After editing any file in `specs/`, sync the installable skill references:

```bash
python3 scripts/sync_skill_refs.py
```

## Manual Install Fallback

If your environment does not have `npx skills`, install manually:

```bash
mkdir -p ~/.codex/skills
cp -R skills/android-finance-spec ~/.codex/skills/
```

## Skill Package

```text
skills/android-finance-spec/
  SKILL.md
  agents/openai.yaml
  references/
    finance-number-skill.md
    rtl-adaption.md
    kotlin-style.md
  scripts/
    android_finance_scan.py
```

## Examples

```text
examples/
  bad-android-finance/
  fixed-android-finance/
```

Use these examples to demo the scanner, test future rule changes, and create before/after screenshots for social sharing.

## Specs

This repository bundles three Android finance engineering specs:

1. **[Financial precision spec](./specs/finance-number-skill.md)**  
   Standardizes amount, percentage, asset quantity, fee, rate, PnL, and balance handling. Financial decimals must use `String` or `BigDecimal`, never `Double` / `Float`.
2. **[RTL and i18n adaptation spec](./specs/rtl-adaption.md)**  
   Covers `start` / `end` layouts, LTR isolation for signs, percentages, dates, currency pairs, and mixed text, plus no hardcoded visible copy.
3. **[Kotlin style and AI generation constraints](./specs/kotlin-style.md)**  
   Enforces project-first architecture, Kotlin/Android style, MVI/MVVM consistency, coroutine/Flow safety, null-safety, and no reinvented project helpers.

## Agent Integration

Use a thin entry file in each target Android project. The entry file should point the agent to `specs/` instead of duplicating every rule.

### Codex

Create `AGENTS.md` in the target project:

```md
# AGENTS.md

You are a senior Android + Kotlin engineer. This project must follow:

- `specs/finance-number-skill.md`
- `specs/rtl-adaption.md`
- `specs/kotlin-style.md`

MUST and MUST NOT rules are hard gates.
Before adding new code, search for existing architecture, helpers, wrappers, naming, and utilities.
Do not invent missing base classes, extension functions, abstractions, or dependencies.
```

### Claude Code

Create `CLAUDE.md` in the target project:

```md
# CLAUDE.md

This is an Android Kotlin finance app.

Before code generation, refactoring, or review, read:

1. `specs/finance-number-skill.md`
2. `specs/rtl-adaption.md`
3. `specs/kotlin-style.md`

All MUST and MUST NOT rules are mandatory.
If a general spec conflicts with existing project implementation or tool configuration, follow the existing project implementation and tool configuration.
```

### Cursor

Create `.cursor/rules/android-finance.mdc`:

```md
---
description: Android Kotlin finance precision, RTL/i18n, and project style rules
globs:
  - "**/*.kt"
  - "**/*.xml"
  - "**/*.java"
alwaysApply: true
---

This project must follow:

- @specs/finance-number-skill.md
- @specs/rtl-adaption.md
- @specs/kotlin-style.md

When generating, editing, or reviewing Android code, enforce every MUST and MUST NOT rule.
Before adding new code, search for existing project patterns and reuse current architecture, wrappers, and tool configuration.
```

### GitHub Copilot

Create `.github/copilot-instructions.md`:

```md
# GitHub Copilot Instructions

When generating or editing Kotlin/Android code, follow:

- `specs/finance-number-skill.md`
- `specs/rtl-adaption.md`
- `specs/kotlin-style.md`

Prefer existing project architecture, package structure, naming, MVI conventions, Repository patterns, Result/error handling, coroutine helpers, and Flow collection style.
Do not add duplicate abstractions or dependencies when existing implementations can be reused.
```

## Recommended Project Layout

```text
your-android-project/
  AGENTS.md
  CLAUDE.md
  .cursor/
    rules/
      android-finance.mdc
  .github/
    copilot-instructions.md
  specs/
    finance-number-skill.md
    rtl-adaption.md
    kotlin-style.md
```

## Shareable Card

Use these files for README images, social previews, technical group sharing, or GitHub issue / PR promotion:

```text
share/android-finance-skill-card.html
share/android-finance-skill-card.png
```

Recommended screenshot ratio: `16:9`.
