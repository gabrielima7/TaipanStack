from urllib.parse import quote

import pytest
from hypothesis import given
from hypothesis import strategies as st

from taipanstack.core.result import Err
from taipanstack.security.guards import guard_ssrf
from taipanstack.security.validators import validate_url


@given(
    st.text(
        alphabet=st.characters(
            max_codepoint=32,
            categories=["Cc", "Cf", "Cs", "Co", "Cn"],
            exclude_characters=set(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~"
            ),
        ),
        min_size=1,
        max_size=5,
    ),
    st.integers(min_value=2, max_value=10),
)
def test_taipanstack_validators_url_recursive_unquote_expected(payload, depth):
    # Control character/invalid character hidden behind `depth` layers of URL encoding
    for _ in range(depth):
        payload = quote(payload)

    url = f"https://example.com/page?q={payload}"

    with pytest.raises(
        ValueError,
        match="URL contains invalid characters|URL exceeds maximum nested encoding limit",
    ):
        validate_url(url)


@given(
    st.text(
        alphabet=st.characters(
            max_codepoint=32,
            categories=["Cc", "Cf", "Cs", "Co", "Cn"],
            exclude_characters=set(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~"
            ),
        ),
        min_size=1,
        max_size=5,
    ),
    st.integers(min_value=2, max_value=10),
)
def test_taipanstack_guards_url_recursive_unquote_expected(payload, depth):
    for _ in range(depth):
        payload = quote(payload)

    url = f"https://example.com/page?q={payload}"

    result = guard_ssrf(url)
    assert isinstance(result, Err)
    assert "URL contains invalid characters" in str(
        result.err()
    ) or "URL exceeds maximum nested encoding limit" in str(result.err())
