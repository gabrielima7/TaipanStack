import pytest
from hypothesis import given, settings, strategies as st
from pydantic import SecretStr
from taipanstack.security.password import verify_password, hash_password

@settings(deadline=None)
@given(st.text(), st.text())
def test_fuzz_verify_password(pw, pw_hash):
    try:
        verify_password(pw, pw_hash)
    except (TypeError, ValueError):
        pass

@settings(deadline=None)
@given(st.one_of(st.text(), st.integers(), st.none(), st.floats(), st.builds(SecretStr, st.text())))
def test_fuzz_hash_password(pw):
    try:
        hash_password(pw)
    except (TypeError, ValueError):
        pass

