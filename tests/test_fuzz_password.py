import contextlib

from hypothesis import given, settings
from hypothesis import strategies as st
from pydantic import SecretStr

from taipanstack.security.password import hash_password, verify_password


@settings(deadline=None)
@given(st.text(), st.text())
def test_fuzz_verify_password_expected(pw, pw_hash):
    with contextlib.suppress(TypeError, ValueError):
        verify_password(pw, pw_hash)

@settings(deadline=None)
@given(st.one_of(st.text(), st.integers(), st.none(), st.floats(), st.builds(SecretStr, st.text())))
def test_fuzz_hash_password_expected(pw):
    with contextlib.suppress(TypeError, ValueError):
        hash_password(pw)
