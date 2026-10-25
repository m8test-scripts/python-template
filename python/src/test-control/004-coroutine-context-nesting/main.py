scope = _coroutines.newScope(None)
timer = _script.getThreads().getMain().getTimer()
captured = "python-nested"
other_task_progress = [False]
def progress(params):
    other_task_progress[0] = True
    _logger.info("nest:python:other-task-progressed")
timer.setTimeout(progress, 50)
def io_context(context):
    context.setDispatcher(lambda dispatchers: dispatchers.getIO())
def script_main_context(context):
    context.setDispatcher(lambda dispatchers: dispatchers.getScriptMain())
def outer_callback(outer):
    if captured != "python-nested":
        raise RuntimeError("outer capture unavailable")
    _logger.info("nest:python:outer-started")
    def inner_callback(inner):
        if captured != "python-nested":
            raise RuntimeError("nested capture unavailable")
        _logger.info("nest:python:inner-callback")
    scope.launch(script_main_context, None, inner_callback)
    if captured != "python-nested":
        raise RuntimeError("outer capture not restored")
    _logger.info("nest:python:outer-resumed")
scope.launch(io_context, None, outer_callback)
def delayed(value):
    if not other_task_progress[0] or captured != "python-nested":
        raise RuntimeError("delay state mismatch")
    _logger.info("nest:python:delay-resumed")
scope.delay(200).onSuccess(delayed)
def gate(params):
    _logger.info("nest:python:gate")
    scope.cancel("done")
timer.setTimeout(gate, 1500)
