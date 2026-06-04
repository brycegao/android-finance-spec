# Android 项目编码规范 Spec | AI-First 编码约束仓库
> 适配 Cursor / Claude Code / CodeX AI 自动编码、代码审查、静态纠错，Android Kotlin 金融类项目专用规范库

## 仓库介绍
本仓库收纳两套项目强制编码规范，面向**跨境金融App（多语言+RTL阿拉伯/波斯/希伯来）**，所有规范采用 `MUST / MUST NOT` 标准化语法，AI 可自动解析约束，编码生成与CR校验自动落地规范，用于统一团队编码口径、规避线上精度bug、RTL布局错乱、多语言漏翻译等高频问题。

### 包含两大规范文档
1. **[金融高精度数值规范](./specs/finance-number-skill.md)**
统一金额、百分比、币种运算规则，杜绝Double/Float浮点丢失精度，全链路`String`存值+BigDecimal运算+统一格式化工具`NumericFormat`。
2. **[RTL国际化多语言适配规范](./specs/rtl-global-spec.md)**
适配阿拉伯语、波斯语、希伯来语等RTL从右往左语种，约束布局start/end、数值LTR防翻转、多语言禁止硬编码、TextView统一样式、波斯语行间距修复等全场景规则。
3. **[优化迭代记录](./specs/OPTIMIZE_RECORD.md)**
规范评审优化履历，记录每版修订原因、落地项、后续迭代计划。

## AI 使用指引
1. 项目接入：将本仓库spec文档加入项目AI知识库，Cursor/Claude可实时读取规范；
2. 编码生成：AI生成布局、业务代码自动遵循MUST强制规则，违规代码直接拦截；
3. CodeReview：提交代码时AI自动对照规范检查，命中禁止项直接标注驳回。

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