# Claude Code 说明

在本仓库生成或修改 Kotlin/Android 代码时，必须遵循项目统一代码规范：

- `specs/kotlin-style.md`

项目内已有实现和工具配置优先级高于通用 Kotlin 或 Android 建议。新增抽象前，必须先检索仓库中是否已有同类模式并优先复用。不要臆造项目中不存在的封装、基类、扩展函数、依赖或架构组件。

修改代码后，在条件允许时使用仓库已有的 ktlint、detekt 或构建检查进行验证。
