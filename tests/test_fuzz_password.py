from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.password import LEGACY_FORMAT, verify_password


@given(
    password=st.text(),
    iterations=st.integers(min_value=1, max_value=10**20),
    salt=st.binary(min_size=1, max_size=100),
    hash_bytes=st.binary(min_size=1, max_size=100),
)
@settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_verify_password_pbkdf2(password, iterations, salt, hash_bytes):
    # Construct a legacy hash string
    salt_hex = salt.hex()
    hash_hex = hash_bytes.hex()
    password_hash = f"{LEGACY_FORMAT}$sha256${iterations}${salt_hex}${hash_hex}"

    # After hardening, verify_password should catch OverflowError and return False
    result = verify_password(password, password_hash)
    assert isinstance(result, bool)


def test_fuzz_password_massive_iterations_explicit():
    password_hash = f"{LEGACY_FORMAT}$sha256$100000000000000000000000000000000$00$00"
    result = verify_password("test", password_hash)
    assert result is False
