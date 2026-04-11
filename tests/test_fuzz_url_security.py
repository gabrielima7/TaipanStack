import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import MAX_URL_LENGTH, validate_url


@settings(
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large],
    max_examples=200,
)
@given(st.text(min_size=MAX_URL_LENGTH + 1, max_size=MAX_URL_LENGTH + 1000))
def test_fuzz_url_massive_strings_dos(url: str) -> None:
    """Fuzz validate_url with massive strings to ensure DoS protection limits are active."""
    with pytest.raises(ValueError, match="URL length exceeds maximum allowed"):
        validate_url(url)


@settings(suppress_health_check=[HealthCheck.filter_too_much])
@given(
    st.text(
        alphabet=st.characters(
            blacklist_categories=("Cc",), whitelist_characters=["\x00"]
        ),
        min_size=10,
        max_size=100,
    ).filter(lambda s: "\x00" in s)
)
def test_fuzz_url_null_bytes(url: str) -> None:
    """Fuzz validate_url with strings containing null bytes."""
    with pytest.raises(ValueError, match="URL contains invalid characters"):
        validate_url(url)


@settings(suppress_health_check=[HealthCheck.filter_too_much])
@given(
    st.text(
        alphabet=st.characters(
            blacklist_characters=["\x00"], min_codepoint=0x200B, max_codepoint=0x200F
        ),
        min_size=1,
        max_size=10,
    )
)
def test_fuzz_url_unprintable_chars(chars: str) -> None:
    """Fuzz validate_url with zero-width characters and unprintable unicode."""
    url = f"http://example.com/{chars}"
    with pytest.raises(ValueError, match="URL contains invalid characters"):
        validate_url(url)


def test_url_port_integer_conversion_dos() -> None:
    """Explicitly test huge port sizes that crash URL parsers."""
    url = "http://example.com:" + "9" * 10000
    with pytest.raises(ValueError, match="URL length exceeds maximum allowed"):
        validate_url(url)


def test_url_tld_ipv6_handling() -> None:
    """Ensure validate_url uses parsed.hostname for localhost checks on IPv6."""
    url = "http://[::1]"
    # Should not raise
    assert validate_url(url) == url


def test_url_credentials_bypassing_tld_check() -> None:
    """Ensure credentials don't mess up the TLD checks because of manual splits on netloc."""
    url = "http://user:pass@notlocalhost"
    # missing TLD, and not localhost, so should raise
    with pytest.raises(ValueError, match="URL domain must have a TLD"):
        validate_url(url)
