# Android 项目编码规范 Spec | AI-First 编码约束仓库
> 适配 Cursor / Claude Code / CodeX AI 自动编码、代码审查、静态纠错，Android Kotlin 金融类项目专用规范库

## 仓库介绍
国际化多语言适配、金融小数高精度处理是跨境金融App开发必备刚需，Cursor、Claude、CodeX等不同AI模型编码风格、实现逻辑参差不齐，相同需求容易产出多版不一致代码，极易引发浮点精度丢失、RTL布局错乱、外文展示异常、文案无法多语言翻译等线上故障。

本仓库沉淀**标准化MUST/MUST NOT强制编码规范**，一套规则约束所有AI，统一AI代码生成口径，实现AI编码、Code Review全流程自动合规，从源头规避金融与国际化高频缺陷。
规范分为两大核心文档，适配Android Kotlin金融项目。

### 包含规范文档
1. **[金融高精度数值规范](./specs/finance-number-skill.md)**
统一金额、百分比、币种运算规则，杜绝Double/Float浮点丢失精度，全链路`String`存值+BigDecimal运算+统一格式化工具`NumericFormat`。
2. **[RTL国际化多语言适配规范](./specs/rtl-adaption.md)**
适配阿拉伯语、波斯语、希伯来语等RTL从右往左语种，约束布局start/end、数值LTR防翻转、多语言禁止硬编码、TextView统一样式、波斯语行间距修复等全场景规则。

## AI 使用指引
1. 项目接入：将本仓库spec文档加入项目AI知识库，Cursor/Claude可实时读取规范；
2. 编码生成：AI生成布局、业务代码自动遵循MUST强制规则，违规代码直接拦截；
3. CodeReview：提交代码时AI自动对照规范检查，命中禁止项直接标注驳回。

## 快速接入

推荐在目标 Android 项目中保留统一 `specs/` 目录，再为不同 AI 工具添加薄入口文件。入口文件只负责声明“必须读取 specs”，不要复制完整规则，避免多份提示词发散。

### 1. 复制规范目录

将本仓库 `specs/` 目录复制到目标项目根目录：

```text
your-android-project/
  specs/
    finance-number-skill.md
    rtl-adaption.md
```

### 2. Codex 接入

在目标项目根目录新增 `AGENTS.md`：

```md
# AGENTS.md

你是资深 Android + Kotlin 工程师，当前项目必须遵守以下规范：

- 金融数值处理必须读取并遵守 `specs/finance-number-skill.md`
- RTL / 多语言适配必须读取并遵守 `specs/rtl-adaption.md`
- 生成代码、重构、Code Review 时，命中 MUST NOT 规则必须主动修复或驳回
- 金融小数字段禁止使用 Double / Float
- UI 可见文案禁止硬编码
```

### 3. Claude Code 接入

在目标项目根目录新增 `CLAUDE.md`：

```md
# CLAUDE.md

本项目是 Android Kotlin 金融类 App。

每次进行代码生成、重构、Review 前，必须先读取：

1. `specs/finance-number-skill.md`
2. `specs/rtl-adaption.md`

所有 MUST / MUST NOT 规则视为强制约束。
如代码与规范冲突，以 specs 文档为准。
```

### 4. Cursor 接入

在目标项目新增 `.cursor/rules/android-finance.mdc`：

```md
---
description: Android Kotlin 金融数值与 RTL 国际化强制规范
globs:
  - "**/*.kt"
  - "**/*.xml"
  - "**/*.java"
alwaysApply: true
---

本项目必须遵守：

- @specs/finance-number-skill.md
- @specs/rtl-adaption.md

生成、修改、Review Android 代码时，必须执行 specs 中的 MUST / MUST NOT 规则。
```

### 5. 推荐目录结构

```text
your-android-project/
  AGENTS.md
  CLAUDE.md
  .cursor/
    rules/
      android-finance.mdc
  specs/
    finance-number-skill.md
    rtl-adaption.md
```

## 规范核心能力总结
### 1. 金融数值规范核心管控点
- 金融金额、涨跌、成交量**禁止Double/Float**，全链路`String`承载原始数值
- 统一`NumericFormat`格式化输出，自动内置`keepLTR`适配RTL
- 全场景运算依托BigDecimal，固定30位预留精度，规避多级乘除精度损耗

### 2. RTL多语言规范核心管控点
- 布局全量`start/end`替换`left/right`，自动跟随系统语种切换方向
- 价格/日期/币对自动LTR隔离，防止RTL文字反转、正负号错位
- 统一TextView四件套：`textSize/textColor/fontFamily/includeFontPadding=false`，解决波斯语多行行距异常
- 全页面文案禁止硬编码，统一多语言资源引用，参数文案使用{0}占位符
