from taipanstack.utils.logging import REDACTED_VALUE, _redact


def test_redact_circular_reference():
    d = {"name": "test"}
    d["self"] = d
    redacted = _redact(d)
    assert redacted["name"] == "test"
    assert redacted["self"] == REDACTED_VALUE

def test_redact_list():
    test_list = [{"password": "123"}, "safe"]
    redacted = _redact(test_list)
    assert redacted[0]["password"] == REDACTED_VALUE
    assert redacted[1] == "safe"

def test_redact_tuple():
    test_tuple = ({"secret": "abc"}, 42)
    redacted = _redact(test_tuple)
    assert redacted[0]["secret"] == REDACTED_VALUE
    assert redacted[1] == 42

def test_redact_no_regex(monkeypatch):
    monkeypatch.setattr("taipanstack.utils.logging._SENSITIVE_KEY_REGEX", None)
    obj = {"password": "123"}
    assert _redact(obj) is obj
