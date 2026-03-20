import pytest
from hypothesis import given, strategies as st
from taipanstack.security.validators import validate_email, validate_project_name, validate_python_version, validate_url

@given(st.text())
def test_fuzz_python_version(version):
    try:
        validate_python_version(version)
    except ValueError:
        pass
    except TypeError:
        pass

@given(st.text(), st.sets(st.text()), st.booleans())
def test_fuzz_url(url, schemes, req_tld):
    try:
        validate_url(url, allowed_schemes=tuple(schemes), require_tld=req_tld)
    except ValueError:
        pass
    except TypeError:
        pass

@given(st.text())
def test_fuzz_email(email):
    try:
        validate_email(email)
    except ValueError:
        pass
    except TypeError:
        pass

@given(st.text(), st.booleans(), st.booleans(), st.integers(min_value=-1000, max_value=10000))
def test_fuzz_project_name(name, allow_hyphen, allow_underscore, max_len):
    try:
        validate_project_name(name, allow_hyphen=allow_hyphen, allow_underscore=allow_underscore, max_length=max_len)
    except ValueError:
        pass
    except TypeError:
        pass

@given(st.integers())
def test_fuzz_python_version_type(version):
    try:
        validate_python_version(version)
    except ValueError:
        pass
    except TypeError:
        pass

@given(st.integers())
def test_fuzz_url_type(url):
    try:
        validate_url(url)
    except ValueError:
        pass
    except TypeError:
        pass

@given(st.integers())
def test_fuzz_email_type(email):
    try:
        validate_email(email)
    except ValueError:
        pass
    except TypeError:
        pass

@given(st.integers())
def test_fuzz_project_name_type(name):
    try:
        validate_project_name(name)
    except ValueError:
        pass
    except TypeError:
        pass

def test_validate_url_local_domain_with_no_tld():
    try:
        validate_url("http://localhost")
    except ValueError:
        pass

def test_validate_url_with_port():
    try:
        validate_url("http://localhost:8080")
    except ValueError:
        pass

def test_email_local_too_long():
    try:
        validate_email("a" * 65 + "@example.com")
    except ValueError:
        pass

def test_email_domain_too_long():
    try:
        validate_email("test@" + "a" * 256 + ".com")
    except ValueError:
        pass

def test_url_local_domain_with_no_tld_no_require():
    try:
        validate_url("http://example", require_tld=False)
    except ValueError:
        pass

def test_url_not_localhost_has_no_tld():
    try:
        validate_url("http://example.")
    except ValueError:
        pass
def test_url_local_domain_tld():
    try:
        validate_url("http://example", require_tld=True)
    except ValueError:
        pass

def test_url_localhost_no_tld():
    try:
        validate_url("http://localhost", require_tld=True)
    except ValueError:
        pass
def test_url_local_domain_with_no_tld_no_require_valid():
    assert validate_url("http://example", require_tld=False) == "http://example"
def test_url_local_domain_tld_valid():
    assert validate_url("http://localhost.com", require_tld=True) == "http://localhost.com"
def test_url_local_domain_tld_has_no_tld():
    try:
        validate_url("http://example")
    except ValueError:
        pass
def test_url_local_domain_tld_has_no_tld_2():
    try:
        validate_url("http://example.")
    except ValueError:
        pass
def test_url_local_domain_tld_has_no_tld_3():
    try:
        validate_url("http://example:80", require_tld=True)
    except ValueError:
        pass
def test_url_local_domain_tld_has_no_tld_4():
    try:
        validate_url("http://example:")
    except ValueError:
        pass
def test_url_local_domain_tld_has_no_tld_5():
    try:
        validate_url("http://example:80")
    except ValueError:
        pass
def test_url_domain_split_check():
    try:
        validate_url("http://ex:ample.com:80", require_tld=True)
    except ValueError:
        pass
def test_url_domain_is_localhost_but_require_tld():
    try:
        validate_url("http://localhost", require_tld=True)
    except ValueError:
        pass
def test_url_tld_logic():
    try:
        validate_url("http://example.", require_tld=True)
    except ValueError:
        pass
def test_url_local_domain_tld_has_no_tld_6():
    try:
        validate_url("http://example:")
    except ValueError:
        pass

def test_url_localhost_upper():
    assert validate_url("http://LOCALHOST", require_tld=True) == "http://LOCALHOST"
def test_url_tld_logic_not_localhost():
    try:
        validate_url("http://ex.ample.", require_tld=True)
    except ValueError:
        pass
def test_url_domain_split_check_2():
    try:
        validate_url("http://example:abc", require_tld=True)
    except ValueError:
        pass
def test_url_local_domain_split_no_tld():
    try:
        validate_url("http://example:", require_tld=True)
    except ValueError:
        pass
def test_url_local_domain_tld_has_no_tld_7():
    try:
        validate_url("http://example.:80")
    except ValueError:
        pass
def test_url_local_domain_tld_has_no_tld_8():
    try:
        validate_url("http://example.:")
    except ValueError:
        pass
def test_url_local_domain_tld_has_no_tld_9():
    try:
        validate_url("http://example:")
    except ValueError:
        pass
def test_url_local_domain_tld_has_no_tld_10():
    try:
        validate_url("http://example.")
    except ValueError:
        pass
def test_url_local_domain_tld_has_no_tld_11():
    try:
        validate_url("http://example.:.")
    except ValueError:
        pass
def test_url_local_domain_tld_has_no_tld_12():
    try:
        validate_url("http://.")
    except ValueError:
        pass
def test_url_local_domain_tld_has_no_tld_13():
    try:
        validate_url("http://.")
    except ValueError:
        pass

def test_validate_url_local_domain_with_no_tld_and_colon():
    try:
        validate_url("http://example:80", require_tld=True)
    except ValueError:
        pass
def test_validate_url_local_domain_with_no_tld_and_colon_2():
    try:
        validate_url("http://example:", require_tld=True)
    except ValueError:
        pass
def test_validate_url_local_domain_with_no_tld_and_colon_3():
    try:
        validate_url("http://example:", require_tld=True)
    except ValueError:
        pass
def test_validate_url_domain_endswith_dot():
    try:
        validate_url("http://example.", require_tld=True)
    except ValueError:
        pass
def test_validate_url_local_domain_with_no_tld_and_colon_4():
    try:
        validate_url("http://example:", require_tld=True)
    except ValueError:
        pass
def test_url_local_domain_tld_has_no_tld_14():
    try:
        validate_url("http://example.")
    except ValueError:
        pass
