from m8test_java.java.lang.StringBuilder import StringBuilder
from m8test_java.com.m8test.script.GlobalVariables import _logger, _arrays, _iterables, _objectWrappers
builder = StringBuilder("M8Test")
builder.append(" Python")
if str(builder.toString()) != "M8Test Python": raise AssertionError("JVM StringBuilder")
raw = _arrays.intArrayOf(3, 1, 2)
values = _objectWrappers.wrapIntArray(raw)
if values.getSize() != 3: raise AssertionError("wrapped size")
values.set(0, 7)
if not values.contains(7): raise AssertionError("wrapped array")
callback_called = []
_logger.withContext(lambda context: callback_called.append(context is not None))
if not callback_called or not callback_called[0]: raise AssertionError("Kotlin function callback")
items = _iterables.listOf("first", "second")
if str(items.get(1)) != "second": raise AssertionError("host List factory")
_logger.info("python-template-jvm-interop:passed")
