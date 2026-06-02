from collections.abc import MutableMapping

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.utils.logging import _redact, _redact_dict, _redact_set


@given(
    value=st.dictionaries(
        st.one_of(
            st.text(),
            st.integers(),
            st.floats(),
            st.none(),
            st.booleans(),
            st.dates(),
            st.datetimes(),
        ),
        st.one_of(
            st.text(),
            st.integers(),
            st.floats(),
            st.none(),
            st.booleans(),
            st.dates(),
            st.datetimes(),
        ),
    )
)
@settings(max_examples=1000, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_logging_redact_fuzz_redact_dict_extreme_keys_expected(value):
    """Bombard _redact_dict with extreme, non-string keys to test resilience.

    Keys generated include None, integers, floats, booleans, dates, and datetimes.
    The function should gracefully skip non-string keys instead of raising a TypeError.
    """
    # We need a copy because hypothesis strategies give us read-only views sometimes,
    # or we might mutate the input dict and break hypothesis' assumptions if not careful,
    # but _redact_dict takes a MutableMapping and mutates it in place.
    # Actually hypothesis gives new dicts for each example.
    mutable_value = dict(value)
    _redact_dict(mutable_value)


@settings(max_examples=1000, suppress_health_check=[HealthCheck.too_slow])
@given(
    st.recursive(
        st.one_of(
            st.text(),
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.booleans(),
            st.none(),
            st.binary(),
        ),
        lambda children: st.one_of(
            st.lists(children),
            st.dictionaries(st.text(), children),
            st.tuples(children, children),
        ),
        max_leaves=10,
    )
)
def test_fuzz_logging_redact_does_not_crash_expected(data: object) -> None:
    """Fuzz test to ensure _redact never crashes on arbitrary nested structures."""
    try:
        _redact(data)
    except Exception as e:
        raise AssertionError(f"Exception raised during redaction: {e}") from e


@settings(max_examples=1000, suppress_health_check=[HealthCheck.too_slow])
@given(st.dictionaries(st.text(), st.text(), min_size=1))
def test_fuzz_logging_redact_dict_does_not_crash_expected(
    data: MutableMapping[str, object],
) -> None:
    """Fuzz test to ensure _redact_dict never crashes on arbitrary dicts."""
    try:
        _redact_dict(data)
    except Exception as e:
        raise AssertionError(
            f"Exception raised during dictionary redaction: {e}"
        ) from e


def test_fuzz_logging_redact_redact_set_standard():
    seen = set()
    s = {"secret_val", 123}
    redacted = _redact_set(s, seen)
    assert redacted == {"secret_val", 123}


def test_fuzz_logging_redact_redact_set_recursive_expected():
    from taipanstack.utils.logging import _redact

    s = {"secret_val"}
    res = _redact(s)
    assert res == {"secret_val"}


class UnhashableMock:
    def __init__(self, val):
        self.val = val

    def __hash__(self):
        # Only raise TypeError during redaction, not during set creation
        if getattr(self, "_in_redact", False):
            raise TypeError("unhashable")
        return hash(self.val)

    def __eq__(self, other):
        return isinstance(other, UnhashableMock) and self.val == other.val

    def __str__(self):
        return f"UnhashableMock({self.val})"


def test_fuzz_logging_redact_redact_set_unhashable_expected():
    from taipanstack.utils.logging import _redact_set

    seen = set()
    mock = UnhashableMock("test_secret")
    s = {mock}
    mock._in_redact = True  # make it unhashable for redaction
    redacted = _redact_set(s, seen)
    assert len(redacted) == 1
    assert "UnhashableMock(test_secret)" in redacted


class StringMock:
    def __init__(self, val):
        self.val = val


def test_fuzz_logging_redact_redact_string_standard():
    from taipanstack.utils.logging import _is_sensitive

    assert not _is_sensitive(StringMock("test"), None)


class UnhashableMockStr:
    def __init__(self, val):
        self.val = val

    def __hash__(self):
        if getattr(self, "_in_redact", False):
            raise TypeError("unhashable")
        return hash(self.val)

    def __eq__(self, other):
        return isinstance(other, UnhashableMockStr) and self.val == other.val

    def __str__(self):
        return "unhashable_str"


def test_fuzz_logging_redact_redact_set_unhashable_branch():
    from taipanstack.utils.logging import _redact_set

    seen = set()
    mock = UnhashableMockStr("test")
    s = {mock}
    mock._in_redact = True
    redacted = _redact_set(s, seen)
    assert len(redacted) == 1
    assert "unhashable_str" in redacted


def test_fuzz_logging_redact_is_sensitive_non_string_expected():
    import re

    from taipanstack.utils.logging import _is_sensitive

    assert not _is_sensitive(123, re.compile("test"))
