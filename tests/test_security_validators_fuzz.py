import contextlib

import hypothesis.strategies as st
from hypothesis import given, settings

from taipanstack.security.validators import (
    validate_email,
    validate_project_name,
    validate_python_version,
    validate_url,
)


@settings(max_examples=500)
@given(st.text())
def test_fuzz_validate_email(s):
    with contextlib.suppress(ValueError):
        validate_email(s)

@settings(max_examples=500)
@given(st.text())
def test_fuzz_validate_url(s):
    with contextlib.suppress(ValueError):
        validate_url(s)

@settings(max_examples=500)
@given(st.text())
def test_fuzz_validate_project_name(s):
    with contextlib.suppress(ValueError):
        validate_project_name(s)

@settings(max_examples=500)
@given(st.text())
def test_fuzz_validate_python_version(s):
    with contextlib.suppress(ValueError):
        validate_python_version(s)
