scope = _coroutines.newScope(None)
timeout_scope = _coroutines.newScope(None)
nullable_scope = _coroutines.newScope(None)
timed_loop_scope = _coroutines.newScope(None)
normal_loop_scope = _coroutines.newScope(None)
composed_scope = _coroutines.newScope(None)
timer = _script.getThreads().getMain().getTimer()
recovery_called = [False]


def recover(scope, error):
    recovery_called[0] = True
    return scope.resolve("fallback")


def unexpected_timeout_success(value):
    raise RuntimeError("timeout unexpectedly succeeded")


def preserve_timeout(error):
    if recovery_called[0]:
        raise RuntimeError("cancellation was recovered")
    _logger.info("coroutine:python:timeout-cancellation-preserved")


timeout_scope.withTimeout(75, lambda s: s.delay(1000)).catchError(recover).onSuccess(
    unexpected_timeout_success
).onError(preserve_timeout)


def assert_null(value):
    if value is not None:
        raise RuntimeError("withTimeoutOrNull did not return None")
    _logger.info("coroutine:python:timeout-or-null-ok")


nullable = nullable_scope.withTimeoutOrNull(75, lambda s: s.delay(1000))
def unexpected_nullable_error(error):
    raise RuntimeError("withTimeoutOrNull failed: " + str(error))


nullable.onSuccess(assert_null).onError(unexpected_nullable_error).onComplete(
    lambda: _logger.info("coroutine:python:timeout-or-null-complete")
)


timed_loop_calls = [0]


def timed_iteration(s):
    timed_loop_calls[0] += 1
    return s.delay(1000).then(lambda inner, ignored: inner.resolve(True))


def timed_loop_error(error):
    if timed_loop_calls[0] != 1:
        raise RuntimeError("timed loop iteration count mismatch")
    _logger.info("coroutine:python:loop-timeout-cancelled-wait")


timed_loop_scope.loopWithTimeout(75, timed_iteration).onError(timed_loop_error)

loop_calls = [0]


def iteration(s):
    loop_calls[0] += 1
    _logger.info("coroutine:python:loop-iteration:" + str(loop_calls[0]))
    return s.resolve(loop_calls[0] < 3)


def loop_complete():
    if loop_calls[0] != 3:
        raise RuntimeError("loop did not finish after three iterations")
    _logger.info("coroutine:python:loop-completed-count:3")


normal_loop_scope.loop(iteration).onComplete(loop_complete)


def assert_composed(value):
    if value is None or int(value) != 23:
        raise RuntimeError("composed wait returned the wrong value")
    _logger.info("coroutine:python:composed-wait-ok")


composed = composed_scope.withTimeoutOrNull(
    500, lambda s: s.delay(25).then(lambda inner, ignored: inner.resolve(23))
)
composed.onSuccess(assert_composed).onComplete(
    lambda: _logger.info("coroutine:python:composed-wait-complete")
)

timer.setTimeout(lambda params: (scope.cancel("done"), _logger.info("coroutine:python:cancellation-gate")), 3000)

runOnUiThread(lambda: _logger.info("coroutine:python:ui-thread-callback"))
