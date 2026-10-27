---
name: accessing-jvm-from-python
description: 从 M8Test Python 脚本访问 JVM 类型、调用成员、传递 callback 或使用宿主 wrappers 时使用。
---

# 从 Python 访问 JVM

先查看模板生成的模块/类代理和当前运行时。代码补全或声明文件存在不证明依赖已进入脚本 classloader。公共 wrapper 语义见 `using-host-values-and-wrappers`。

```python
from m8test_java.java.lang.StringBuilder import StringBuilder
from m8test_java.com.m8test.script.GlobalVariables import _arrays, _objectWrappers

builder = StringBuilder("M8Test")
builder.append(" Python")
assert builder.toString() == "M8Test Python"

raw = _arrays.intArrayOf(3, 1, 2)
values = _objectWrappers.wrapIntArray(raw)
values.set(0, 7)
assert values.getSize() == 3 and values.contains(7)
```

Python `int`、`None`、list 与 JVM primitive、nullable、数组/集合不能仅凭相似性互换。函数 callback 与 overload 按生成代码和目标 JVM 签名验证。修改示例时更新本模板的 JVM interop fixture，并使用真实运行时验证。
