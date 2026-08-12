import hypothesis.strategies as st
import pytest
from hypothesis import given

from taipanstack.security.guards import _validate_env_var_name


@given(st.text(min_size=0, max_size=10).filter(lambda s: not s.strip()))
def test_env_var_empty_name(name):
    with pytest.raises(Exception, match=""):
        _validate_env_var_name(name)
