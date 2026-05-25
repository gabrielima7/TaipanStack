def test_core_optimizations_additional_core_optimizations_apply_gc_threshold_exception():
    from unittest.mock import patch

    from taipanstack.core.optimizations import OptimizationProfile, _apply_gc_tuning

    profile = OptimizationProfile()
    errors = []
    applied = []

    with patch(
        "taipanstack.core.optimizations.gc.set_threshold",
        side_effect=Exception("mocked error"),
    ):
        _apply_gc_tuning(profile, applied, errors)

    assert len(errors) == 1
    assert "gc_threshold: mocked error" in errors[0]


def test_core_optimizations_additional_core_optimizations_apply_gc_freeze_exception():
    from unittest.mock import patch

    from taipanstack.core.optimizations import OptimizationProfile, _apply_gc_freeze

    profile = OptimizationProfile(gc_freeze_enabled=True)
    errors = []
    applied = []
    skipped = []

    with patch(
        "taipanstack.core.optimizations.gc.freeze",
        side_effect=Exception("mocked error"),
    ):
        with patch("taipanstack.core.optimizations.PY312", True):
            _apply_gc_freeze(profile, True, applied, skipped, errors)

    assert len(errors) == 1
    assert "gc_freeze: mocked error" in errors[0]


def test_core_optimizations_additional_core_optimizations_apply_experimental_flags():
    from unittest.mock import MagicMock, patch

    from taipanstack.core.optimizations import OptimizationProfile, _apply_experimental

    profile = OptimizationProfile(enable_experimental=True)
    applied = []
    skipped = []

    mock_features = MagicMock()
    mock_features.has_jit = True
    mock_features.has_free_threading = True

    with patch(
        "taipanstack.core.optimizations.get_features", return_value=mock_features
    ):
        _apply_experimental(profile, applied, skipped)

    assert "jit: available" in applied
    assert "free_threading: available" in applied


def test_core_optimizations_additional_core_optimizations_apply_experimental_flags_false():
    from unittest.mock import MagicMock, patch

    from taipanstack.core.optimizations import OptimizationProfile, _apply_experimental

    profile = OptimizationProfile(enable_experimental=True)
    applied = []
    skipped = []

    mock_features = MagicMock()
    mock_features.has_jit = False
    mock_features.has_free_threading = False

    with patch(
        "taipanstack.core.optimizations.get_features", return_value=mock_features
    ):
        _apply_experimental(profile, applied, skipped)

    assert "jit: available" not in applied
    assert "free_threading: available" not in applied


def test_core_optimizations_additional_core_optimizations_logging_branches():
    from unittest.mock import patch

    from taipanstack.core.optimizations import _log_optimization_summary

    with patch("taipanstack.core.optimizations.logger") as mock_logger:
        _log_optimization_summary(["app"], ["skip"], ["err"])

        mock_logger.debug.assert_any_call("Applied optimizations: %s", "app")
        mock_logger.debug.assert_any_call("Skipped optimizations: %s", "skip")
        mock_logger.warning.assert_called_with("Optimization errors: %s", "err")


def test_core_optimizations_additional_core_optimizations_apply_optimizations_skipped_false():
    from unittest.mock import patch

    from taipanstack.core.optimizations import OptimizationProfile, apply_optimizations

    profile = OptimizationProfile(enable_experimental=True)
    with patch("taipanstack.core.optimizations._apply_experimental") as mock_exp:

        def side_effect(p, a, s):
            a.append("fake")

        mock_exp.side_effect = side_effect
        res = apply_optimizations(profile=profile, apply_gc=False)
        assert res.success is True


def test_core_optimizations_additional_core_optimizations_missing_optimizations_skipped():
    from unittest.mock import MagicMock, patch

    from taipanstack.core.optimizations import OptimizationProfile, apply_optimizations

    profile = OptimizationProfile(enable_perf_hints=True, enable_experimental=True)
    mock_features = MagicMock()
    mock_features.has_jit = True
    mock_features.has_free_threading = True

    with patch(
        "taipanstack.core.optimizations.get_features",
        return_value=mock_features,
    ):
        res = apply_optimizations(profile=profile)
        assert len(res.skipped) == 0


def test_core_optimizations_additional_core_optimizations_apply_optimizations_with_errors():
    import gc
    from unittest.mock import patch

    from taipanstack.core.optimizations import OptimizationProfile, apply_optimizations

    profile = OptimizationProfile()

    with patch.object(gc, "set_threshold", side_effect=RuntimeError("boom")):
        result = apply_optimizations(profile=profile, apply_gc=True)

    assert not result.success
    assert len(result.errors) > 0
    assert any("boom" in e for e in result.errors)
