"""Tests for missing branch coverage in optimizations."""

from taipanstack.core.optimizations import OptimizationProfile, apply_optimizations


def test_optimizations_apply_optimizations_skipped_empty_returns_success() -> None:
    """Test that apply_optimizations handles an empty 'skipped' list correctly."""
    from unittest.mock import MagicMock, patch

    mock_profile = MagicMock(spec=OptimizationProfile)
    mock_profile.enable_perf_hints = True
    mock_profile.enable_experimental = True

    with (
        patch(
            "taipanstack.core.optimizations.get_optimization_profile",
            return_value=mock_profile,
        ),
        patch("taipanstack.core.optimizations._apply_gc_tuning"),
        patch("taipanstack.core.optimizations._apply_gc_freeze"),
        patch("taipanstack.core.optimizations.get_features") as mock_features,
    ):
        # Configure features so _apply_experimental appends to 'applied' but not 'skipped'
        features_mock = MagicMock()
        features_mock.has_jit = True
        features_mock.has_free_threading = True
        mock_features.return_value = features_mock

        result = apply_optimizations(
            apply_gc=True, freeze_after=True, force_refresh=True
        )

        assert result.success is True
        assert len(result.skipped) == 0
