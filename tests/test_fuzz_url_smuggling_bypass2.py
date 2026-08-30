import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.core.result import Err
from taipanstack.security.guards import SecurityError, guard_ssrf
from taipanstack.security.validators import validate_url


@settings(max_examples=100)
@given(st.integers(min_value=11, max_value=20))
def test_url_smuggling_bypass_validators(depth: int) -> None:
    payload = "%00"
    for _ in range(depth):
        payload = payload.replace("%", "%25")
    url = f"http://example.com/{payload}"
    with pytest.raises(
        ValueError, match="URL contains invalid characters|nested encoding limit"
    ):
        validate_url(url)


@settings(max_examples=100)
@given(st.integers(min_value=11, max_value=20))
def test_url_smuggling_bypass_guards(depth: int) -> None:
    payload = "%00"
    for _ in range(depth):
        payload = payload.replace("%", "%25")
    url = f"http://example.com/{payload}"
    result = guard_ssrf(url)
    assert isinstance(result, Err)
    assert isinstance(result.err_value, SecurityError)
    assert "URL contains invalid characters" in str(
        result.err_value
    ) or "nested encoding limit" in str(result.err_value)
