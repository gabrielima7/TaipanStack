from taipanstack.security.models import (
    SecureBaseModel,
    _mask_collection,
    _mask_data,
    _mask_list,
    _mask_set,
    _mask_tuple,
)
from taipanstack.utils.logging import REDACTED_VALUE


def test_security_models_kwargs():
    class TestKwargsModel(SecureBaseModel):
        field: str

    obj = TestKwargsModel(field="value")
    # Test kwargs to hit lines like 130 and 175
    dumped = obj.model_dump(exclude_unset=True, round_trip=True, warnings=False)
    assert dumped["field"] == "value"

    dumped_json = obj.model_dump_json(exclude_unset=True, round_trip=True, warnings=False)
    assert "value" in dumped_json

def test_security_models_str_key_in_is_sensitive_key():
    from taipanstack.security.models import _is_sensitive_key
    assert not _is_sensitive_key(123)

def test_security_models_fallback_and_others():
    class EdgeModel(SecureBaseModel):
        key: str

    obj = EdgeModel(key="val")
    dumped = obj.model_dump(include={"key"}, exclude=None, context={"foo": "bar"}, by_alias=True, exclude_defaults=True, exclude_none=True, exclude_computed_fields=True, fallback=lambda x: x, serialize_as_any=True)
    assert dumped["key"] == "val"

    dumped_json = obj.model_dump_json(include={"key"}, exclude=None, context={"foo": "bar"}, by_alias=True, exclude_defaults=True, exclude_none=True, exclude_computed_fields=True, fallback=lambda x: x, serialize_as_any=True, ensure_ascii=True)
    assert "val" in dumped_json

def test_security_models_str_and_repr_args():
    class TestModel(SecureBaseModel):
        normal_key: str
        password: str

    obj = TestModel(normal_key="normal", password="secret")
    repr_args = list(obj.__repr_args__())
    assert ("normal_key", "normal") in repr_args
    assert ("password", REDACTED_VALUE) in repr_args

def test_security_models_mask_list():
    lst = ["normal", {"password": "secret"}]
    res = _mask_list(lst, 0)
    assert res[0] == "normal"
    assert res[1]["password"] == REDACTED_VALUE

def test_security_models_mask_tuple():
    t = ("normal", {"password": "secret"})
    res = _mask_tuple(t, 0)
    assert res[0] == "normal"
    assert res[1]["password"] == REDACTED_VALUE

def test_security_models_mask_set():
    s = {"normal", "data"}
    res = _mask_set(s, 0)
    assert "normal" in res

def test_security_models_str():
    class TestStrModel(SecureBaseModel):
        password: str
    obj = TestStrModel(password="secret")
    assert REDACTED_VALUE in str(obj)

def test_security_models_indent():
    class TestIndentModel(SecureBaseModel):
        password: str
    obj = TestIndentModel(password="secret")
    assert "\n" in obj.model_dump_json(indent=4)

def test_security_models_mask_list_of_lists():
    data = [["data"]]
    res = _mask_collection(data, 0)
    assert res == [["data"]]

def test_security_models_mask_tuple_of_tuples():
    data = (("data",),)
    res = _mask_collection(data, 0)
    assert res == (("data",),)

def test_security_models_mask_set_of_sets():
    data = frozenset({"data"})
    res = _mask_collection({data}, 0)
    assert data in res

def test_security_models_max_depth_hit():
    res = _mask_data("test", 101)
    assert res == "<MAX_DEPTH_REACHED>"

def test_security_models_none_regex(monkeypatch):
    from taipanstack.security import models
    monkeypatch.setattr(models, "_SENSITIVE_KEY_REGEX", None)
    res = models._mask_data({"a": "b"}, 0)
    assert res == {"a": "b"}
