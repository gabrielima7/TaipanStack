import pytest
from hypothesis import given, settings, HealthCheck, strategies as st
from taipanstack.security.sanitizers import sanitize_filename, sanitize_path, sanitize_env_value, sanitize_sql_identifier

@settings(
    max_examples=500,
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large]
)
@given(st.text())
def test_fuzz_sanitize_filename(text):
    try:
        res = sanitize_filename(text)
        assert isinstance(res, str)
        assert len(res) <= 255
    except Exception as e:
        if not isinstance(e, (ValueError, TypeError)):
            raise

@settings(
    max_examples=500,
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large]
)
@given(st.text())
def test_fuzz_sanitize_sql_identifier(text):
    try:
        res = sanitize_sql_identifier(text)
        assert isinstance(res, str)
    except Exception as e:
        if not isinstance(e, (ValueError, TypeError)):
            raise

if __name__ == "__main__":
    pytest.main(["-v", "test_fuzz_sanitizers_dos.py"])
