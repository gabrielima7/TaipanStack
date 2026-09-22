"""Property-based tests for serialization utilities."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from taipanstack.core.result import Err, Ok
from taipanstack.utils.serialization import default_encoder

# Strategy for valid JSON-serializable primitives and collections
json_strategy = st.recursive(
    st.none()
    | st.booleans()
    | st.floats(allow_nan=False, allow_infinity=False)
    | st.integers()
    | st.text(),
    lambda children: st.lists(children) | st.dictionaries(st.text(), children),
    max_leaves=10,
)


class TestSerializationFuzzing:
    """Fuzzing tests for default_encoder."""

    @given(st.dictionaries(st.text().filter(lambda x: x != "status"), json_strategy))
    def test_utils_serialization_fuzz_ok_with_dict_expected(
        self, data: dict[str, object]
    ) -> None:
        """Test default_encoder with Ok containing dict."""
        res = Ok(data)
        encoded_dict = default_encoder(res)
        assert isinstance(encoded_dict, dict)
        assert encoded_dict.get("status") == "success"
        # Validate that all elements in original dict are present in encoded_dict
        for k, v in data.items():
            assert encoded_dict.get(k) == v

    @given(json_strategy.filter(lambda x: not isinstance(x, dict)))
    def test_utils_serialization_fuzz_ok_with_non_dict_expected(
        self, data: object
    ) -> None:
        """Test default_encoder with Ok containing non-dict."""
        res = Ok(data)
        encoded_dict = default_encoder(res)
        assert isinstance(encoded_dict, dict)
        assert encoded_dict.get("status") == "success"
        assert encoded_dict.get("data") == data

    @given(st.text() | st.integers() | st.builds(Exception, st.text()))
    def test_utils_serialization_fuzz_err_expected(self, error_value: object) -> None:
        """Test default_encoder with Err containing various error types."""
        res = Err(error_value)
        encoded_dict = default_encoder(res)
        assert isinstance(encoded_dict, dict)
        assert encoded_dict.get("status") == "error"
        assert encoded_dict.get("message") == str(error_value)

    @given(json_strategy)
    def test_utils_serialization_fuzz_unsupported_type(self, data: object) -> None:
        """Test default_encoder with unsupported types directly."""
        with pytest.raises(TypeError, match="is not JSON serializable"):
            default_encoder(data)
