scope = _coroutines.newScope(None)
timer = _script.getThreads().getMain().getTimer()
def script_main_context(context):
    context.setName("script-main")
    context.setDispatcher(lambda dispatchers: dispatchers.getScriptMain())
    if context.getName() != "script-main":
        raise RuntimeError("coroutine context name mismatch")
def script_main_callback(s):
    if not _script.getThreads().getCurrent().isCurrent():
        raise RuntimeError("script-main dispatcher mismatch")
    _logger.info("coroutine:python:script-main-verified")
scope.launch(script_main_context, None, script_main_callback)
captured_script_value = "python-captured"
other_task_progress = [False]
def progress_other_task(params):
    other_task_progress[0] = True
    _logger.info("coroutine:python:other-task-progressed")
timer.setTimeout(progress_other_task, 50)
def io_context(context):
    context.setDispatcher(lambda dispatchers: dispatchers.getIO())
def io_callback(s):
    if captured_script_value != "python-captured":
        raise RuntimeError("captured script value mismatch")
    _logger.info("coroutine:python:io-captured-value-verified")
scope.launch(io_context, None, io_callback)
def delayed_callback(value):
    if captured_script_value != "python-captured":
        raise RuntimeError("delayed script value mismatch")
    if not other_task_progress[0]:
        raise RuntimeError("other task did not progress during delay")
    _logger.info("coroutine:python:delayed-captured-value-verified")
scope.delay(200).onSuccess(delayed_callback)
scope.launch(None, None, lambda s: _logger.info("coroutine:python:launch"))
def verify_async_value(value):
    if int(value) != 7:
        raise RuntimeError("async value mismatch: " + str(value))
    _logger.info("coroutine:python:async-success")
scope._async(None, None, lambda s: (_logger.info("coroutine:python:async"), 7)[1]).onSuccess(verify_async_value)
scope.withContext(lambda context: None, lambda s: (_logger.info("coroutine:python:with-context"), 9)[1])
def map_value(s, value):
    _logger.info("coroutine:python:flow:" + str(value))
    return s.resolve(value * 2)
def verify_mapped_values(values):
    if len(values) != 2 or int(values[0]) != 2 or int(values[1]) != 4:
        raise RuntimeError("flow mapped values mismatch")
    _logger.info("coroutine:python:flow-complete")
_coroutines.getFlows().of(1, 2).map(map_value).toList(scope).onSuccess(verify_mapped_values)
scope.delay(5000).onComplete(lambda: _logger.info("coroutine:python:cancelled-work-complete"))
timer.setTimeout(lambda params: ( _logger.info("coroutine:python:gate"), scope.cancel("done")), 1500)
