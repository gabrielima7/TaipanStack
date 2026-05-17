import string
from hypothesis import given, strategies as st
from taipanstack.security.validators import validate_python_version, validate_email, validate_url

@given(st.text(), st.text(), st.text())
def test_fuzz_url_domain(scheme, host, path):
    try:
        url = f"{scheme}://{host}/{path}"
        validate_url(url)
    except (ValueError, TypeError):
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "fuzz_script8.py"])
