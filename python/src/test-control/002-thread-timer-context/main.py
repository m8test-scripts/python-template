timer = _script.getThreads().getMain().getTimer()
timeout_args = [False]
immediate_done = [False]
worker = [False]
count = [0]
interval_id = [0]
nested_result = timer.runWithThreadContext(
    lambda: timer.runWithThreadContext(lambda: "nested"))
if nested_result != "nested":
    raise RuntimeError("nested thread context result mismatch")
def on_immediate(params):
    immediate_done[0] = True
    _logger.info("thread-context:python:immediate")
def fail_immediate(params):
    raise RuntimeError("expected timer callback failure")
timer.setImmediate(on_immediate)
def on_timeout(params):
    if len(params) != 2 or params[0] != "payload" or params[1] is not None:
        raise RuntimeError("timeout arguments mismatch")
    timeout_args[0] = True
    _logger.info("thread-context:python:timeout")
timer.setTimeout(on_timeout, 100, "payload", None)
cancelled_timeout = timer.setTimeout(lambda params: fail_immediate(params), 1000)
timer.clearTimeout(cancelled_timeout)
cancelled_immediate = timer.setImmediate(lambda params: fail_immediate(params))
timer.clearImmediate(cancelled_immediate)
def on_interval(params):
    if len(params) != 1 or params[0] != "tick":
        raise RuntimeError("interval arguments mismatch")
    count[0] += 1
    if count[0] == 2:
        timer.clearInterval(interval_id[0])
        _logger.info("thread-context:python:interval")
interval_id[0] = timer.setInterval(on_interval, 75, "tick")
def on_thread_start(thread):
    if not thread.isCurrent() or thread.isMain() or not thread.isAlive() or thread.isInterrupted() or str(thread.getName()) != "thread-context-worker":
        raise RuntimeError("thread start context mismatch")
    _logger.info("thread-context:python:thread-start")
def on_thread_exit(thread):
    if not thread.isCurrent() or thread.isMain() or not thread.isAlive() or thread.isInterrupted() or str(thread.getName()) != "thread-context-worker":
        raise RuntimeError("thread exit context mismatch")
    _logger.info("thread-context:python:thread-exit")
_script.getThreads().onStart(on_thread_start)
_script.getThreads().onExit(on_thread_exit)
def on_worker(thread):
    worker[0] = True
    _logger.info("thread-context:python:thread")
_script.getThreads().start("thread-context-worker", on_worker)
def verify(params):
    if nested_result != "nested" or not timeout_args[0] or not immediate_done[0] or not worker[0] or count[0] != 2:
        raise RuntimeError("timer callback state mismatch")
    _logger.info("thread-context:python:verified")
timer.setTimeout(verify, 500)
