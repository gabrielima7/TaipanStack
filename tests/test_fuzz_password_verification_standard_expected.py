import hypothesis.strategies as st
from hypothesis import HealthCheck, given, settings

from taipanstack.security.password import verify_password


@given(
    pw=st.text(min_size=1, max_size=100), hash_suffix=st.text(min_size=1, max_size=2000)
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_password_verification_argon2_malformed_returns_false_standard_expected(pw, hash_suffix):
    """Bombard verify_password with valid prefixes but malformed suffix data."""
    malformed_hash = "$argon2id$v=19$m=65536,t=3,p=4$" + hash_suffix
    # Should cleanly return False, not raise VerificationError
    assert verify_password(pw, malformed_hash) is False
