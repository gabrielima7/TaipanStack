import pytest

from taipanstack.core.result import Ok
from taipanstack.utils.cache import cached


def test_security_cache_unbounded_security_cache_bounded():
    """Verify that the cache size is strictly bounded by max_size."""
    max_size = 10

    @cached(ttl=60.0, max_size=max_size)
    def get_data(i: int):
        return Ok(i)

    # Call with more than max_size unique keys
    for i in range(max_size * 2):
        get_data(i)

    # Access internal _cache
    cells = get_data.__closure__
    cache_dict = None
    for cell in cells:
        val = cell.cell_contents
        if isinstance(val, dict) and len(val) == max_size:
            cache_dict = val
            break

    assert cache_dict is not None
    assert len(cache_dict) == max_size

    # Check if LRU works: access an old but not yet evicted item
    @cached(ttl=60.0, max_size=3)
    def lru_test(i: int):
        return Ok(i)

    lru_test(1)  # [1]
    lru_test(2)  # [1, 2]
    lru_test(1)  # [2, 1] - 1 moved to end
    lru_test(3)  # [2, 1, 3]
    lru_test(4)  # [1, 3, 4] - 2 evicted because it was at the front

    cells = lru_test.__closure__
    cache_dict = None
    for cell in cells:
        val = cell.cell_contents
        if isinstance(val, dict) and len(val) == 3:
            cache_dict = val
            break

    assert cache_dict is not None
    # Verify key for 2 is NOT in cache_dict
    key_for_2 = ("lru_test", (2,), ())
    assert key_for_2 not in cache_dict
    assert ("lru_test", (1,), ()) in cache_dict
    assert ("lru_test", (3,), ()) in cache_dict
    assert ("lru_test", (4,), ()) in cache_dict


@pytest.mark.asyncio
async def test_security_cache_unbounded_security_cache_bounded_async():
    """Verify async cache bounding and LRU."""
    max_size = 5

    @cached(ttl=60.0, max_size=max_size)
    async def get_data_async(i: int):
        return Ok(i)

    for i in range(max_size + 2):
        await get_data_async(i)

    cells = get_data_async.__closure__
    cache_dict = None
    for cell in cells:
        val = cell.cell_contents
        if isinstance(val, dict) and len(val) == max_size:
            cache_dict = val
            break

    assert cache_dict is not None
    assert len(cache_dict) == max_size


def test_security_cache_unbounded_security_cache_validation():
    """Verify max_size validation."""
    with pytest.raises(ValueError, match="max_size must be a positive integer"):

        @cached(ttl=60.0, max_size=0)
        def func1():
            return None

    with pytest.raises(ValueError, match="max_size must be a positive integer"):

        @cached(ttl=60.0, max_size=-1)
        def func2():
            return None

    with pytest.raises(ValueError, match="max_size must be a positive integer"):

        @cached(ttl=60.0, max_size="10")  # type: ignore
        def func3():
            return None

    with pytest.raises(ValueError, match="max_size must be a positive integer"):

        @cached(ttl=60.0, max_size=True)  # type: ignore
        def func4():
            return None
