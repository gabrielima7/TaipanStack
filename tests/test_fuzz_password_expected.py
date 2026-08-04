from hypothesis import given, settings
from hypothesis import strategies as st
from pydantic import SecretStr

from taipanstack.security.password import hash_password, verify_password


@settings(deadline=None)
@given(st.text(), st.text())
def test_fuzz_password_fuzz_verify_password_returns_bool_or_raises_error(pw, pw_hash):
    try:
        result = verify_password(pw, pw_hash)
        assert isinstance(result, bool)
    except (TypeError, ValueError):
        assert True


@settings(deadline=None)
@given(
    st.one_of(
        st.text(),
        st.integers(),
        st.none(),
        st.floats(),
        st.builds(SecretStr, st.text()),
    )
)
def test_fuzz_password_fuzz_hash_password_returns_str_or_raises_error(
    pw,
):
    try:
        result = hash_password(pw)
        assert isinstance(result, str)
    except (TypeError, ValueError):
        assert True
