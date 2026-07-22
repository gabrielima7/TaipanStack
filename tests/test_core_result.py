

def test_core_result_collect_iterable_unreachable():
    """Test _collect_iterable with unreachable logic."""
    from taipanstack.core.result import _collect_iterable
    # Passing something that is neither Ok nor Err, but within an iterable
    # Since python 3.12 match statement doesn't type check structural fallbacks
    res = _collect_iterable(["invalid"])  # type: ignore
    assert res == "invalid"
