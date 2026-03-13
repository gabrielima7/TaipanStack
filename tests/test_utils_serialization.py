"""Tests for serialization utilities."""

import orjson
import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.utils.serialization import default_encoder


class TestDefaultEncoder:
    """Tests for the default_encoder with orjson."""

    def test_encode_ok_with_dict(self) -> None:
        """Test encoding Ok containing a dict."""
        res = Ok({"data": 1})
        encoded = orjson.dumps(res, default=default_encoder)
        assert encoded == b'{"status":"success","data":1}'

        res2 = Ok({"user": "test", "id": 42})
        encoded2 = orjson.dumps(res2, default=default_encoder)
        assert encoded2 == b'{"status":"success","user":"test","id":42}'

    def test_encode_ok_with_scalar(self) -> None:
        """Test encoding Ok containing a scalar or list."""
        res = Ok(42)
        encoded = orjson.dumps(res, default=default_encoder)
        assert encoded == b'{"status":"success","data":42}'

        res_str = Ok("text")
        encoded_str = orjson.dumps(res_str, default=default_encoder)
        assert encoded_str == b'{"status":"success","data":"text"}'

        res_list = Ok([1, 2, 3])
        encoded_list = orjson.dumps(res_list, default=default_encoder)
        assert encoded_list == b'{"status":"success","data":[1,2,3]}'

    def test_encode_err(self) -> None:
        """Test encoding Err."""
        res = Err(ValueError("something went wrong"))
        encoded = orjson.dumps(res, default=default_encoder)
        assert encoded == b'{"status":"error","message":"something went wrong"}'

        res_str = Err("string error")
        encoded_str = orjson.dumps(res_str, default=default_encoder)
        assert encoded_str == b'{"status":"error","message":"string error"}'

    def test_encode_unsupported_type(self) -> None:
        """Test encoding an unsupported type."""

        class CustomObj:
            pass

        with pytest.raises(
            orjson.JSONEncodeError, match="Type is not JSON serializable: CustomObj"
        ):
            orjson.dumps(CustomObj(), default=default_encoder)

    def test_default_encoder_direct_type_error(self) -> None:
        """Test calling default_encoder directly with unsupported types."""
        with pytest.raises(TypeError, match="Type str is not JSON serializable"):
            default_encoder("string")

        with pytest.raises(TypeError, match="Type int is not JSON serializable"):
            default_encoder(42)

        with pytest.raises(TypeError, match="Type list is not JSON serializable"):
            default_encoder([1, 2, 3])

    def test_encode_ok_with_status_override(self) -> None:
        """Test encoding Ok where dict contains 'status' key."""
        # The 'status' key in the dict will override the default 'success'
        res = Ok({"status": "overridden", "data": 1})
        encoded = orjson.dumps(res, default=default_encoder)
        assert encoded == b'{"status":"overridden","data":1}'
