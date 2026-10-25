timer = _script.getThreads().getMain().getTimer()
def fail(params):
    _logger.info("thread-context:python:timer-error")
    raise RuntimeError("expected timer callback failure")
timer.setImmediate(fail)
