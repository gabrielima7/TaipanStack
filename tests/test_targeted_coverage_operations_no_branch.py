
def test_optimization_gc_freeze_enabled_but_not_freeze_after(monkeypatch):
    import taipanstack.core.optimizations as opts
    monkeypatch.setattr(opts, "PY312", True)
    # mock gc.freeze
    import gc
    monkeypatch.setattr(gc, "freeze", lambda: None)
    profile = opts.OptimizationProfile(gc_freeze_enabled=True)
    res = opts.apply_optimizations(profile=profile, apply_gc=False, freeze_after=False)
    assert res.success is True

def test_apply_optimizations_nothing_skipped(monkeypatch):
    import taipanstack.core.optimizations as opts
    monkeypatch.setattr(opts, "PY312", True)
    import gc
    monkeypatch.setattr(gc, "freeze", lambda: None)
    monkeypatch.setattr(gc, "set_threshold", lambda *_args: None)

    class MockFeatures:
        has_jit = True
        has_free_threading = True

    monkeypatch.setattr(opts, "get_features", lambda *_args, **_kwargs: MockFeatures())

    profile = opts.OptimizationProfile(
        gc_freeze_enabled=True,
        enable_experimental=True,
        enable_perf_hints=True
    )

    res = opts.apply_optimizations(profile=profile, apply_gc=True, freeze_after=True)
    assert len(res.skipped) == 0


def test_circuit_breaker_match_fallthrough():
    from taipanstack.resilience.circuit_breaker import CircuitBreaker
    cb = CircuitBreaker(name="test")
    cb._state.state = "INVALID_STATE"  # type: ignore[assignment]
    cb._record_success()
    cb._record_failure(Exception("test"))

def test_process_path_part_empty_result(monkeypatch):
    import taipanstack.security.sanitizers as san
    monkeypatch.setattr(san, "_is_safe_path_part", lambda _p, _s: False)
    monkeypatch.setattr(san, "sanitize_filename", lambda _p, **_kwargs: "")

    parts = []
    san._process_path_part("bad", parts, "/")
    assert parts == [] # safe_part is empty, so it doesn't append

def test_process_path_part_dot(monkeypatch):
    import taipanstack.security.sanitizers as san
    parts = []
    san._process_path_part(".", parts, "/")
    assert parts == [] # branch `elif part != ".":` evaluates to False, doing nothing
