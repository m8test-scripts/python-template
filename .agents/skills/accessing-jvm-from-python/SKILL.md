---
name: accessing-jvm-from-python
description: 当 Python 脚本需要访问 JVM 类、调用 Java/Kotlin 成员或传递函数 callback 时使用。
---

# 从 Python 访问 JVM

Python JVM 类通过 m8test_java.<package>.<Class> 模块路径导入；宿主全局变量从生成的 GlobalVariables 模块导入。模板 init/AccessJvm.py 展示类和 callback 调用。

## 类与对象

```python
from m8test_java.java.lang.StringBuilder import StringBuilder
builder = StringBuilder("M8Test")
builder.append(" Python")
assert str(builder.toString()) == "M8Test Python"
```

先确认依赖已加载到当前脚本 classloader。声明文件或代码补全存在不等于运行时类可见。方法重载、静态字段、嵌套类、异常等边界按目标语言的生成代码和实际设备行为验证。

## 函数 callback

单表达式可用 lambda；多语句 callback 用 def。Python callable 与 JVM SAM 的兼容性以目标签名和设备实测为准。

## 函数 callback 示例

Python lambda 可以按目标 Kotlin 函数类型传入 callback。模板 Test Control 通过 Logger.withContext 实际验证 callback 被调用并获得参数：

```python
called = []
_logger.withContext(lambda context: called.append(context is not None))
assert called and called[0]
```

## 类型转换边界

Python int、float、str、None、list 与 JVM 类型并不等价。不要假设 Python list 自动转换为 JVM array/List；按目标签名使用宿主工厂并验证。

逐项记录已测试的 primitive/boxed、字符串、nullable、数组、集合、varargs、重载和异常行为。未经执行验证的转换写为待验证，不根据其他脚本语言推断。

## 验证

本模板的 python-template-jvm-interop Test Control 场景会实际调用 JVM StringBuilder，并验证宿主数组工厂和 wrapper。运行当前项目支持的选中 Test Control 任务并检查 summary 中该 requestId 为 passed；若当前模板没有注册相应任务，使用模板设备运行任务并确认成功日志。Gradle 使用 -q。
