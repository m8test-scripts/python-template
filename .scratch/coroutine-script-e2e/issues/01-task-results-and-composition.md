# 01: 验收任务结果、同步配置与异步组合

Type: task
Status: ready-for-agent

**What to build:** Python 真实脚本通过 Test Control 证明任务创建、精确结果、错误恢复和组合等待。

**Blocked by:** 00：验收原有 Thread/Timer 的真实脚本基线


## 前置公开能力

- 目标语言可用的统一基础执行与协程 API

能力未具备时不能启动交付；本项目不定义或重建这些通用契约。

## Acceptance criteria

- [ ] 用稳定 manifest 与独立脚本运行，包含同步 builder、启动选择器、launch/async、结果链、nullable 与集合。
- [ ] 覆盖 delay、超时、循环及实际公开组合方法；建立可复用的有限事件等待与失败报告方式。
- [ ] 脚本实际断言之后才输出标记，最终响应与清理均成功才通过；测试源码保持产品发布隔离。

## Comments

基础上下文和嵌套上下文用例通过真实 Test Control，分别验证 `getScriptMain()`、IO、delay 后闭包访问、等待期间 Timer 推进，以及嵌套 launch 前后闭包状态。重新运行取消/超时组合场景后通过，日志覆盖超时取消、nullable 超时、循环取消等待、组合等待与 gate；此前记录的连续读取超时未复现。完整逐方法 API 证据仍需继续补齐。

`002-thread-timer-context` 的线程生命周期断言现也通过：worker 的 `onStart` 与 `onExit` callback 检查 `isCurrent()`、`isMain()` 和 `getName()`，并继续验证 runnable、Timer 参数、interval 两轮后取消及嵌套 context。

该用例进一步断言生命周期回调期间线程仍 `isAlive()` 且 `isInterrupted()` 为假，设备 Test Control 通过。

`003-coroutine-thread-context` 现断言 `_async` 返回值为 `7`，且 Flow `map/toList` 结果为 `[2, 4]`；Python 侧按原生序列用 `len` 和索引检查，设备 Test Control 通过。
