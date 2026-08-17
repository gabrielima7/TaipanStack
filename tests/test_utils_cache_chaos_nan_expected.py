import math

import pytest

from taipanstack.utils.cache import cached


def test_utils_cache_chaos_nan_cache_ttl_nan_mutation_graceful_degradation_expected():
    """
    Simulate a rare production failure where the `ttl` state of the cached decorator
    gets corrupted/mutated to NaN (math.nan).
    The system should safely degrade by raising a ValueError immediately at decorator binding time,
    preventing infinite loops or corrupted state in the cache dictionary.
    """
    with pytest.raises(ValueError, match="ttl must be a finite non-negative number"):

        @cached(ttl=math.nan)
        def dummy_function():
            return "ok"


def test_utils_cache_chaos_nan_cache_ttl_inf_mutation_graceful_degradation_expected():
    """
    Simulate corruption of `ttl` to math.inf.
    """
    with pytest.raises(ValueError, match="ttl must be a finite non-negative number"):

        @cached(ttl=math.inf)
        def dummy_function():
            return "ok"


def test_utils_cache_chaos_nan_cache_ttl_negative_mutation_graceful_degradation_expected():
    """
    Simulate corruption of `ttl` to a negative number.
    """
    with pytest.raises(ValueError, match="ttl must be a finite non-negative number"):

        @cached(ttl=-1.0)
        def dummy_function():
            return "ok"


def test_utils_cache_chaos_nan_cache_ttl_type_mutation_graceful_degradation_expected():
    """
    Simulate corruption of `ttl` to a non-numeric type.
    """
    with pytest.raises(ValueError, match="ttl must be a finite non-negative number"):

        @cached(ttl="30")  # type: ignore[arg-type]
        def dummy_function():
            return "ok"
