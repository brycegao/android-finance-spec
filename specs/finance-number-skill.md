# AI CODING SPEC: 金融数值处理强制规范

## META（AI 识别元信息）

- 适用平台：Android / Kotlin
- 适用业务：金融、加密货币、交易、钱包、理财、费率、盈亏、保证金
- 规范等级：**MUST 强制**，AI 编码/重构/Review 100% 遵守
- 适配模型：Cursor / Claude Code / CodeX

---

## 一、核心原则（AI 必须强制执行）

1. **MUST** 存储层：所有金融数值 DTO 使用 `String?`，Gson 读取原始文本，零数值中转、零精度丢失
2. **MUST** 运算层：所有金融计算使用 `BigDecimal`，**MUST NOT** 使用 `Double/Float` 做运算、比较、判等
3. **MUST** 展示层：所有数值格式化统一收口 `NumericFormat`，禁止手写格式化逻辑
4. **MUST** 兜底层：全局 Gson 大数策略 + 空值/非法值逻辑运算结果返回 `null`；UI 展示统一显示 `--`，异常场景强制埋日志，杜绝崩溃、空白、误导性 0 值

---

## 二、全局常量（AI 禁止硬编码）

> CALC_SCALE=24：平衡精度与性能，覆盖主流加密货币 18 位小数 + 1~2 轮乘除中间量溢出

```kotlin
object FinanceConst {
    /** 内部计算最大精度，预留冗余兼容多轮乘除 */
    const val CALC_SCALE = 24
    /** 内部运算舍入：直接截断（撮合、链上结算规则，符合金融风控保守原则） */
    val CALC_ROUND = RoundingMode.DOWN
    /** 展示层舍入：四舍五入（用户账单、资产页、K线等面向用户场景） */
    val DISPLAY_ROUND = RoundingMode.HALF_UP
    /** 空值 / 非法数值 UI 展示占位符 */
    const val DEFAULT_EMPTY_DISPLAY = "--"
}
```

---

## 三、Gson 解析规范（AI 强制配置）

**MUST 唯一金融 Gson 实例**

```kotlin
val financeGson = GsonBuilder()
    .setObjectToNumberStrategy(ToNumberPolicy.BIG_DECIMAL)
    .create()
```

**AI 解析规则**

- DTO `String` 字段：原样读取 JSON 文本，不转换、不丢精度
- `Object` / `Number` 泛型字段：**MUST** 使用 BigDecimal 解析，禁止 Double
- 项目 **MUST NOT** 使用裸 `Gson()` 构造

---

## 四、DTO 字段规约（AI 静态检查）

**MUST 使用 `String?` 的字段**

价格、数量、金额、余额、冻结、手续费、费率、收益率、盈亏、保证金、本息

**MUST NOT 使用**

- `Double?` / `Float?`（完全禁止）
- `Int?` / `Long?`（禁止用于金融计价）

**标准 DTO Demo**

```kotlin
data class ApiOrder(
    val amount: String? = null,
    val price: String? = null,
    val fee: String? = null,
    val feeRate: String? = null,
)
```

**边界规则（AI 自动兜底）**：`null` / 空串 / 非法数字 / `"null"` 参与逻辑运算时结果返回 `null`，UI 展示统一显示 `--`

---

## 五、工程三层架构（AI 固定结构）

### 1. BigDecimalOps（底层原子能力）

提供安全四则运算、精确比较、异常捕获。统一 `CALC_SCALE` 基准精度、默认 `CALC_ROUND`（DOWN 截断）；除法、乘法支持传入自定义 RoundingMode。`safeAction` 捕获除零、格式异常，逻辑运算结果返回 `null`；异常时 **MUST** 打印错误日志（原始入参 + 异常信息）。

### 2. 扩展函数（业务唯一入口）

**String? 扩展**（DTO 主力 API）

- 基础简写：`add / minus / times / div`
- 兼容别名：`plus / subtract / multiply / divide`（方便不同编码习惯）
- 比较：`greaterThan / greaterOrEquals / lessThan / lessOrEquals / equalsByBigDecimal`
- 工具：`toBigDecimalSafe / stripTrailingZeros / decimalPlaces / isValidAmount`
- 特性：空值非法值参与逻辑运算时返回 `null`，UI 格式化层统一展示 `--`，无 NPE
- `isValidAmount` 附加：支持传入最小交易面额，校验是否满足币种最小下单单位

**Number? 扩展**（UI 桥接）

Int/Long/Float/Double 统一转字符串复用 String 整套逻辑，**MUST NOT** 直接浮点运算。

### 3. NumericFormat（唯一格式化层）

AI 生成 UI 展示代码 **MUST** 全部走此类。默认 `DISPLAY_ROUND`（HALF_UP 四舍五入，符合用户直观预期）；内部对账、风控等高精度场景可入参切换 `CALC_ROUND`（DOWN 截断）。统一负数规则：运算原生支持负数字符串，格式化可配置正负前缀 / 括号包裹负数。

能力：千分位、精度截断、K/M/B/T 大数缩写、钱包余额、百分比、极小价零位压缩。

---

## 六、AI 编码标准用法 & 正反示例

**正确示例**

```kotlin
// 运算
val total = order.amount.times(order.price)
// 比较
val isProfit = total.greaterThan("0")
// 格式化（自定义舍入）
val billText = NumericFormat.format(total, 2, roundDown = false, addPrefix = true)
// UI 数值桥接
val realValue = seekBar.progress.times("0.0001")
// 最小金额校验
val canTrade = amount.isValidAmount(minLimit = "0.00000001")
```

**错误 & 修正对照**

| 错误写法 | 修正代码 |
|---------|---------|
| `val total = a.toDouble() * b.toDouble()` | `val total = a.times(b)` |
| `if (num > "0")` | `if (num.greaterThan("0"))` |
| `String.format("%.2f", src)` | `NumericFormat.format(src, 2)` |

---

## 七、AI 禁止反模式（自动拦截）

**MUST NOT 出现以下代码，AI 重构必须自动修复**

| 错误写法 | 问题 | AI 修正方案 |
|---------|------|------------|
| `Double/Float` 接收金额 | 精度丢失 | 替换为 `String?` |
| `BigDecimal(double)` | 构造失真 | 替换为 `BigDecimal(string)` |
| `a.toDouble() + b.toDouble()` | 浮点误差 | 使用扩展 `add/minus/times/div` |
| 字符串直接大小比较 | 字典序错误 | 使用 `greaterThan` 系列方法 |
| `String.format` / `DecimalFormat` 手写 | 隐式丢精度 | 替换为 `NumericFormat` |
| 硬编码 `scale` / 舍入模式 | 不统一 | 使用 `FinanceConst.CALC_SCALE` / `FinanceConst.CALC_ROUND` / `FinanceConst.DISPLAY_ROUND` |

---

## 八、出入参规范（AI 自动适配）

**入参**

- 金融金额、价格、数量、费率等带小数位字段 **MUST** 使用 `String` 或 `BigDecimal` 入参，**MUST NOT** 使用 `Double` / `Float`
- 前端入参禁止千分逗号；使用 `String` 时只允许标准数字字符串
- 兼容标准科学计数 `1E-8`，解析后必须进入 `BigDecimal` 链路

**出参**

- 金融金额、价格、数量、费率等带小数位字段 **MUST** 使用 `String` 或 `BigDecimal` 出参，**MUST NOT** 使用 `Double` / `Float`
- 对外 JSON 为避免客户端精度损失，金融小数字段推荐输出 JSON 字符串（带引号）
- 仅纯整数计数类字段（如条数、页码、毫秒时间戳）可使用 `Int` / `Long`

---

## 九、边界兜底规则（AI 全覆盖）

空值、空串、非法字符、超大数、极小数、科学计数、除零异常、负数场景全覆盖；异常转换 / 除零自动打日志，逻辑运算结果返回 `null`，UI 展示统一显示 `--`，禁止静默归零。

---

## 十、AI CR 强制规则

1. 所有金融数值字段非 `String?` 一律驳回
2. 所有浮点运算一律驳回
3. 所有非规范格式化一律驳回
4. 所有硬编码精度 / 舍入一律驳回
5. 所有不安全 BigDecimal 构造一律驳回
6. 所有空值 / 非法值静默归零一律驳回，必须逻辑返回 `null`、UI 显示 `--`
