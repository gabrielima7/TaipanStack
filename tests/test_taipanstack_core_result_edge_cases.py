import pytest
from taipanstack.core.result import Ok, Err

def test_ok_value_equality_edge_cases():
    ok1 = Ok(None)
    ok2 = Ok(None)
    assert ok1 == ok2
    assert ok1 != Ok(1)
    assert ok1 != Err(None)

def test_err_value_equality_edge_cases():
    err1 = Err("error")
    err2 = Err("error")
    assert err1 == err2
    assert err1 != Err("different")
    assert err1 != Ok("error")
