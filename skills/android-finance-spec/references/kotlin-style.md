# AI CODING SPEC: Kotlin 编码风格强制规范

## META（AI 识别元信息）

- 适用平台：Android / Kotlin
- 适用业务：所有 Android 项目通用
- 规范等级：**MUST 强制**，AI 编码/重构/Review 100% 遵守
- 适配模型：Cursor / Claude Code / CodeX

---

## 一、核心原则（AI 必须强制执行）

1. **MUST** 项目优先级最高：生成或修改代码时，必须优先遵循当前项目已有架构（若项目使用MVVM则延用MVVM，若使用MVI则延用MVI）、目录、命名、封装、依赖注入、异常处理、Result封装、Repository模式和工具配置；若本规范与项目现有实现或ktlint/detekt配置冲突，以项目现有实现和工具配置为准
2. **MUST NOT** 臆造项目中不存在的基类、工具类、扩展函数、统一封装、架构组件或第三方依赖；需要通用能力时，先查找并复用项目已有实现，仅在明确没有可复用实现且业务确实需要时，才新增最小必要封装
3. **MUST** 生成代码前必须先检索项目中是否已有同类实现、命名、封装和目录结构，新增代码必须与现有模式保持一致

---

## 二、代码格式

1. 缩进固定4空格，代码行最大宽度120字符，多行参数/构造必须添加尾随逗号，文件末尾保留空行，去除行尾多余空格
2. 导入顺序优先遵循项目ktlint/IDE配置，禁止*全量导入；若项目未配置，则按Android原生SDK → AndroidX框架 → 第三方开源库 → 项目内部业务包分组，各组之间空一行

---

## 三、命名规则

1. 类、接口、密封类、枚举、Compose可组合函数：PascalCase；普通函数、成员变量、方法参数：camelCase；编译期常量：UPPER_SNAKE_CASE
2. 布尔判断函数统一is/has/can前缀，生命周期回调/点击事件方法on开头；扩展函数按领域或用途归集到*Ext.kt文件，例如ViewExt.kt、FlowExt.kt、StringExt.kt，禁止将无关扩展函数堆到通用Utils文件中
3. StateFlow/LiveData私有字段带下划线_前缀，对外暴露只读无下划线

---

## 四、工程与目录规范

1. 整体分层：UI层 → ViewModel → Domain领域层 → Data数据层
2. 单业务包固定分包：contract(UiState/Intent/Event或ViewModel状态类)、model、widget、adapter，页面Fragment/Activity+ViewModel同业务目录
3. **MUST NOT** UI(Activity/Fragment)直接调用接口、写数据逻辑，网络、本地存取统一下沉至Repository；ViewModel必须通过构造函数注入依赖，禁止内部直接实例化数据层对象

---

## 五、架构与状态规约（MVVM/MVI自适应）

1. 架构跟随项目：严格识别并遵循项目现有架构
2. MVI架构约束：页面状态统一使用sealed interface实现UiState、UiIntent、UiEvent；UiState根据页面复杂度选择实现：简单页面使用密封类穷举状态（Idle/Loading/Success/Error），复杂/分页/局部刷新页面使用data class承载独立状态字段；新代码全部使用StateFlow，不再新增LiveData
3. MVVM架构约束：ViewModel通过StateFlow（首选）或LiveData暴露不可变状态给UI；一次性事件（如Toast、导航）使用SharedFlow或基于LiveData的Event包装类；**MUST NOT** 在ViewModel中暴露可变状态流给UI层

---

## 六、协程与Flow强制约束

1. **MUST** ViewModel使用viewModelScope，Activity/Fragment使用lifecycleScope，**MUST NOT** 使用GlobalScope
2. **MUST** 所有launch启动必须有异常处理兜底：优先使用项目已有的协程异常捕获封装；若项目无现成封装，业务逻辑必须使用 try-catch 包裹并转换为业务 ErrorState，禁止裸 launch；CoroutineExceptionHandler 仅用于根协程全局异常日志兜底，不能替代业务 try-catch；IO耗时逻辑flowOn(Dispatchers.IO)，确保UI更新在主线程调度
3. **MUST** 页面收集Flow必须使用flowWithLifecycle绑定页面生命周期；Flow异常必须在合适层级统一处理或转换为业务Result/ErrorState，禁止无语义地裸抛到UI层

---

## 七、空安全与金融编码强校验

1. 优先定义非空类型，仅数据库/接口不确定字段声明可空；使用?.安全调用、?:默认值兜底，业务代码**MUST NOT** 使用!!非空断言
2. 集合优先不可变listOf/mapOf，取值优先firstOrNull/getOrNull，未证明集合非空时禁用first直接取值；when处理密封类必须穷尽全部分支（Kotlin 1.7+已强制穷尽检查，无需额外exhaustive扩展）
3. **MUST NOT** 使用 Double/Float 承载金额、利率等金融数值，全链路使用 String 传递原始数值，运算必须依托 BigDecimal
4. 优先val，合理控制var使用范围；DataClass仅作为纯数据载体，不嵌入业务逻辑；禁止魔法数字、明文硬编码敏感密钥、账号信息

---

## 八、AI 禁止反模式（自动拦截）

| 禁止写法 | 问题 | AI 修正方案 |
|---------|------|------------|
| `GlobalScope.launch` | 生命周期不受控，内存泄漏 | 使用 viewModelScope / lifecycleScope |
| `val x = obj!!` | NPE 崩溃风险 | 使用 `?.` / `?: 默认值` / `?: return` |
| `val x = list[0]` | IndexOutOfBoundsException | 使用 `list.firstOrNull()` / `getOrNull(0)` |
| Activity 直接调用接口 | 架构越层 | 下沉至 Repository，ViewModel 注入依赖 |
| `Double`/`Float` 承载金融数值 | 精度丢失 | 使用 `String?` + BigDecimal |
| `MutableList`/`MutableMap` 无理由暴露 | 数据不可控 | 优先 `listOf`/`mapOf` 不可变集合 |
| 函数超过80行 | 可读性差 | 抽取子方法，控制嵌套层级 |
| 日志打印敏感信息 | 安全风险 | 脱敏或禁止打印 token/密钥/隐私字段 |

---

## 九、代码结构排序

输出代码结构严格遵循类成员排序：companion object（含const val常量） → 公开属性 → 私有属性 → init初始化块 → 次构造函数(constructor) → 公开方法 → 私有方法 → 内部类/内部接口。（注：主构造函数声明在类头部）

---

## 十、AI CR 强制规则

1. 所有 GlobalScope 使用一律驳回
2. 所有 !! 非空断言一律驳回（仅测试代码允许）
3. 所有架构越层（UI直接调用接口/写数据逻辑）一律驳回
4. 所有 Double/Float 金融数值字段一律驳回
5. 所有裸 launch（无异常处理）一律驳回
6. 所有未绑定生命周期的 Flow 收集一律驳回
