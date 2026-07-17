import pytest

from taipanstack.utils.cache import cached


def test_cache_ttl_coverage():
    with pytest.raises(ValueError, match="ttl must be a finite non-negative number"):
        @cached(ttl=-1)
        def func1():
            pass

    with pytest.raises(ValueError, match="ttl must be a finite non-negative number"):
        @cached(ttl=float("inf"))
        def func2():
            pass

    with pytest.raises(ValueError, match="ttl must be a finite non-negative number"):
        @cached(ttl=float("nan"))
        def func3():
            pass

    with pytest.raises(ValueError, match="ttl must be a finite non-negative number"):
        @cached(ttl="invalid") # type: ignore
        def func4():
            pass
