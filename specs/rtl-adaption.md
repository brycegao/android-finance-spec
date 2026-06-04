# AI CODING SPEC: RTL 多语言适配强制规范

## META

- 适用平台：Android / Kotlin
- 适用业务：面向海外用户的 App，支持阿拉伯语、希伯来语、波斯语等 RTL 语言
- 规范等级：**MUST 强制**，AI 编码/重构/Review 100% 遵守
- 适配模型：Cursor / Claude Code / CodeX

---

## 一、核心原则（AI 必须强制执行）

1. **MUST** 布局使用 `start`/`end` 替代 `left`/`right`，保证视图自动适配语言方向
2. **MUST** 数值文案（价格、涨跌幅、成交量等）调用 `keepLTR()` 强制从左到右渲染，禁止 RTL 翻转数值和 +/- 符号
3. **MUST NOT** 在代码、布局文件里硬编码任何用户可见文案，全部走多语言翻译
4. **MUST NOT** 设置 `android:layoutDirection`，保证子 View 跟随当前语言方向自动切换
5. **MUST** 为每个 TextView 设置字号、字体、字色，禁止依赖全局默认值
6. **MUST** 关闭 `includeFontPadding`，避免阿拉伯语、波斯语多行文本间距与 UI 稿不一致

---

## 二、布局规范

### 2.1 禁止 left/right，MUST 使用 start/end

| 禁止写法 | 必须写法 |
|---------|----------|
| `layout_constraintLeft_toLeftOf` | `layout_constraintStart_toStartOf` |
| `layout_constraintRight_toRightOf` | `layout_constraintEnd_toEndOf` |
| `layout_constraintLeft_toRightOf` | `layout_constraintStart_toEndOf` |
| `layout_constraintRight_toLeftOf` | `layout_constraintEnd_toStartOf` |
| `layout_toLeftOf` | `layout_toStartOf` |
| `layout_toRightOf` | `layout_toEndOf` |
| `layout_marginLeft` | `layout_marginStart` |
| `layout_marginRight` | `layout_marginEnd` |
| `paddingLeft` | `paddingStart` |
| `paddingRight` | `paddingEnd` |
| `drawableLeft` | `drawableStart` |
| `drawableRight` | `drawableEnd` |
| `gravity="left"` | `gravity="start"` |
| `textAlignment="viewLeft"` | `textAlignment="viewStart"` |

### 2.2 禁止设置 layoutDirection

**MUST NOT** 在布局文件或代码中设置 `layoutDirection="rtl"` 或 `layoutDirection="ltr"`。

语言方向切换由 Activity 基类统一控制，子 View 通过继承自动跟随，手动设置会破坏方向传递链。

**唯一例外**：父容器内嵌套 LTR 强制区域（如 WebView、第三方 SDK 容器），MUST 在代码中设置且添加明确注释说明原因。

### 2.3 ConstraintLayout 居中写法

对称居中 MUST 使用 `start`/`end`，禁止 `left`/`right`：

```xml
<!-- 正确 -->
android:layout_constraintStart_toStartOf="parent"
android:layout_constraintEnd_toEndOf="parent"
```

---

## 三、数值 LTR 隔离规范

### 3.1 核心问题

RTL 语言下（阿拉伯语、希伯来语、波斯语），TextView 内容默认从右到左渲染。数值 `"1,234.56"` 会被翻转为 `"65.432,1"`，`+/-` 符号会跑到数字右侧。

### 3.2 keepLTR() 工具函数

**MUST** 对所有数值文案调用 `keepLTR()`，内部使用 Unicode 双向隔离符 LRI(`⁦`) + PDI(`⁩`) 包裹文本，确保内容始终从左到右渲染：

```kotlin
/**
 * 强制文本从左到右渲染，RTL 语言下防止数值、符号翻转
 * 原理：U+2066(LRI) + 原文 + U+2069(PDI) 形成双向隔离
 */
fun String?.keepLTR(): String? {
    return if (isRtl() && !isNullOrEmpty()) {
        "⁦$this⁩"
    } else this
}
```

### 3.3 必须调用 keepLTR() 的场景

- 价格：`"42,156.78 USDT".keepLTR()`
- 涨跌幅：`"+5.23%".keepLTR()` / `"-3.15%".keepLTR()`
- 成交量：`"1,234,567".keepLTR()`
- 数值文案组合：`"最新价 42,156.78".keepLTR()`
- 金额范围：`"100 ~ 50,000".keepLTR()`
- 百分比费率：`"0.1%".keepLTR()`
- 币对名称：`"BTC/USDT".keepLTR()`
- 日期：`"2025-01-15 14:30:00".keepLTR()`

### 3.4 +/- 符号规则

- `+`/`-` **MUST** 始终在数字左侧，跟随数字一起被 `keepLTR()` 包裹
- 数值为 0 时 **MUST** 显示 `0.00%`，**MUST NOT** 显示 `-0.00%` 或 `+0.00%`
- 涨跌符号 **MUST NOT** 单独拼接后裸露在 RTL 上下文中，必须与数值在 `keepLTR()` 内部一起

```kotlin
// 正确：符号和数值整体包裹
val display = "${sign}5.23%".keepLTR()

// 错误：符号单独拼接，RTL 下可能跑到数字右侧
val display = sign + "5.23%".keepLTR()
```

### 3.5 fitRtl() — 非数值内容的 RTL 适配

用户名、地址、邮箱等非数值混合文本，使用 RLM(`‏`) 标记方向：

```kotlin
/**
 * 为非数值文本添加 RTL 方向标记
 * 原理：U+200F(RLM) 告知渲染引擎前文为 RTL
 */
fun String?.fitRtl(): String? {
    return if (isRtl() && !isNullOrEmpty()) "‏$this" else this
}
```

### 3.6 textAdapterRtl() — 地址类长文本

钱包地址、邮箱、手机号等长字符串，使用 LRM(`‎`) 防止被 RTL 引擎拆分：

```kotlin
fun String?.textAdapterRtl(): String? {
    return if (!isNullOrEmpty() && isRtl()) "‎$this" else this
}
```

### 3.7 格式化层集成

`NumericFormat` 等格式化函数 **MUST** 在最终输出时自动调用 `keepLTR()`，业务层无需重复调用：

```kotlin
// NumericFormat 内部已处理 keepLTR，业务层直接使用
val display = NumericFormat.percentage(value, digit = 2, prefix = true)
```

---

## 四、多语言规范

### 4.1 禁止硬编码

**MUST NOT** 在代码或布局文件中出现任何用户可见的硬编码文案：

```kotlin
// 禁止
textView.text = "取消"
textView.text = "Confirm"
binding.tvTitle.text = "登录验证"

// 必须
textView.text = ResUtils.getString(R.string.cancel)
textView.text = getString(R.string.confirm)
```

```xml
<!-- 禁止 -->
<TextView android:text="Name" />
<TextView android:text="取消" />

<!-- 必须 -->
<TextView android:text="@string/name" />
<TextView android:text="@string/cancel" />
```

**例外**：技术缩写（MA、EMA、BOLL、MACD 等指标名）、测试页面。

### 4.2 参数化文案使用 {0}/{1} 占位符

**MUST NOT** 使用字符串拼接，**MUST** 使用占位符：

```kotlin
// 禁止：字符串拼接，翻译脚本无法识别
"本次共答对 $correct 题，答错 $wrong 题"

// 必须：使用 {0}/{1} 占位符，翻译脚本可跨语言处理
ResUtils.getString(R.string.quiz_result).formatWrapper(correct, wrong)
```

`formatWrapper()` 基于 `MessageFormat.format()`，支持单引号转义。

### 4.3 禁止换行符

字符串中 **MUST NOT** 包含 `\n`，需要分行时拆分为多个 key。

---

## 五、TextView 样式规范（含 RTL 字体间距修复）

### 5.1 四要素必填（新增 includeFontPadding）

每个 TextView **MUST** 设置以下 4 个属性，禁止依赖全局默认值：

```xml
<TextView
    android:textSize="@dimen/text_size_14"
    android:textColor="@color/text_primary"
    android:fontFamily="@font/harmony_sans_regular"
    android:includeFontPadding="false" />
```

| 属性 | 说明 |
|------|------|
| `textSize` | 禁止使用 sp 硬编码，MUST 引用 dimen 资源 |
| `textColor` | 禁止硬编码颜色值，MUST 引用 color 资源 |
| `fontFamily` | 禁止使用系统默认字体，MUST 显式指定项目字体 |
| `includeFontPadding` | 必须设为 false，避免波斯语/阿拉伯语多行文本行间距与 UI 不一致 |

### 5.2 字号、字色语义化

MUST 使用语义化资源命名，禁止魔数：

```xml
<!-- 正确：语义化资源 -->
android:textSize="@dimen/text_size_body"
android:textColor="@color/text_primary"

<!-- 禁止：硬编码 -->
android:textSize="14sp"
android:textColor="#FF333333"
```

---

## 六、AI 禁止反模式（自动拦截）

| 禁止写法 | 问题 | AI 修正方案 |
|---------|------|------------|
| `layout_constraintLeft_toLeftOf` | RTL 下不翻转 | 替换为 `Start_toStartOf` |
| `layout_marginLeft` | RTL 下不翻转 | 替换为 `layout_marginStart` |
| `layoutDirection="rtl"` | 破坏方向传递链 | 删除，由 Activity 基类统一控制 |
| 数值文案未调用 `keepLTR()` | RTL 下数值和符号翻转 | 添加 `.keepLTR()` |
| `"+" + amount` 符号单独拼接 | 符号可能在 RTL 下跑到数字右侧 | `"${sign}amount".keepLTR()` |
| 数值为 0 显示 `+0.00%` 或 `-0.00%` | 语义错误 | 格式化函数内部归零，仅显示 `0.00%` |
| 代码中硬编码可见文案 | 无法翻译 | 替换为 `getString(R.string.xxx)` |
| 布局中硬编码可见文案 | 无法翻译 | 替换为 `@string/xxx` |
| 字符串拼接构造参数化文案 | 翻译脚本无法处理 | 使用 `{0}/{1}` 占位符 |
| TextView 未设置 `textSize` | 依赖全局默认不可控 | 设置 `textSize` dimen 资源 |
| TextView 未设置 `textColor` | 依赖全局默认不可控 | 设置 `textColor` color 资源 |
| TextView 未设置 `fontFamily` | 依赖全局默认不可控 | 设置 `fontFamily` 字体资源 |
| `textSize="14sp"` 硬编码 | 无法统一调整 | 引用 `@dimen/xxx` |
| `includeFontPadding="true"` | 波斯语多行文本间距错乱 | 强制改为 `false` |

---

## 七、RTL 适配速查表

| 场景 | 处理方式 |
|------|---------|
| 价格 / 金额 / 数量 | `.keepLTR()` |
| 涨跌幅百分比 | `.keepLTR()` |
| 成交量 / 市值 | `.keepLTR()` |
| 币对名称 BTC/USDT | `.keepLTR()` |
| +/- 符号 | 与数值整体包裹在 `keepLTR()` 内 |
| 数值为 0 | 显示 `0.00%`，禁止 +/- 前缀 |
| 用户名 / 昵称 | `.fitRtl()` |
| 钱包地址 / 邮箱 | `.textAdapterRtl()` |
| 日期时间 | `.keepLTR()` |
| 纯 UI 文案 | 多语言 `getString()` |
| 图标方向 | `drawableStart/End` + `start/end` 约束 |
| 弹窗定位 | 根据 `isRtl()` 切换 Left/Right Popup |
| 波斯语/阿拉伯语多行文本 | `android:includeFontPadding="false"` |

---

## 八、AI CR 强制规则

1. 所有 `left`/`right` 布局属性一律驳回
2. 所有 `layoutDirection` 硬编码一律驳回
3. 所有数值文案未调用 `keepLTR()` 一律驳回
4. 所有硬编码可见文案一律驳回
5. 所有字符串拼接构造参数化文案一律驳回
6. 所有 TextView 未设置字号/字色/字体/includeFontPadding 四项一律驳回
7. 数值为 0 时显示 +/- 前缀一律驳回
8. 所有 `includeFontPadding` 未设为 `false` 一律驳回