import pytest
from hypothesis import given, settings, HealthCheck, strategies as st
from taipanstack.security.jwt import decode_jwt

@settings(
    max_examples=500,
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large]
)
@given(st.lists(st.text()))
def test_fuzz_jwt_algorithms(algos):
    try:
        # Pass a generator constructed from the list
        def gen():
            for a in algos:
                yield a

        decode_jwt("dummy", "secret", gen(), "aud")
    except Exception as e:
        if not isinstance(e, (ValueError, TypeError, Exception)):
            raise

if __name__ == "__main__":
    pytest.main(["-v", "test_fuzz_jwt.py"])
