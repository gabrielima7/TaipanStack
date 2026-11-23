from taipanstack.utils.logging import REDACTED_VALUE, _redact


def test_logging_redact_security_utils_logging_redact_circular_reference_redacted():
    d = {"name": "test"}
    d["self"] = d
    redacted = _redact(d)
    assert redacted["name"] == "test"
    assert redacted["self"] == REDACTED_VALUE


def test_logging_redact_security_utils_logging_redact_list_redacted():
    test_list = [{"password": "123"}, "safe"]
    redacted = _redact(test_list)
    assert redacted[0]["password"] == REDACTED_VALUE
    assert redacted[1] == "safe"


def test_logging_redact_security_utils_logging_redact_tuple_redacted():
    test_tuple = ({"secret": "abc"}, 42)
    redacted = _redact(test_tuple)
    assert redacted[0]["secret"] == REDACTED_VALUE
    assert redacted[1] == 42


def test_logging_redact_security_utils_logging_redact_no_regex_unmodified(
    monkeypatch,
):
    monkeypatch.setattr("taipanstack.utils.logging._SENSITIVE_KEY_REGEX", None)
    obj = {"password": "123"}
    assert _redact(obj) is obj


def test_logging_redact_security_utils_logging_redact_recursion_limit_dos():
    from taipanstack.utils.logging import MAX_DEPTH_VALUE

    data: dict[str, object] = {}
    curr = data
    for _ in range(5000):
        curr["a"] = {}
        curr = curr["a"]  # type: ignore[assignment]

    # This should not raise a RecursionError
    redacted = _redact(data)
    redacted_str = str(redacted)
    assert MAX_DEPTH_VALUE in redacted_str
