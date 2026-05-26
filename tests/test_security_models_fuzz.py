"""Fuzz tests for SecureBaseModel data masking."""

from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.security.models import SecureBaseModel


# Fuzzing target: deeply nested and varied structures containing sensitive keys
@settings(max_examples=200)
@given(
    st.recursive(
        st.dictionaries(st.text(), st.text())
        | st.lists(st.text())
        | st.floats()
        | st.integers()
        | st.none(),
        lambda children: (
            st.dictionaries(st.text(), children)
            | st.lists(children)
            | st.tuples(children)
            | st.sets(st.text())
        ),
        max_leaves=50,
    )
)
def test_security_models_fuzz_masking(payload: object) -> None:
    """Fuzz deeply nested payload masking including tuples and sets."""

    # Construct a payload containing a known sensitive key nested somewhere inside
    class Container(SecureBaseModel):
        payload: object

    model = Container(payload={"nested": ({"password": "secret_password"}, payload)})

    dumped = model.model_dump()

    # Check that "secret_password" is not in the dumped output as a string representation
    dump_str = str(dumped)
    assert "secret_password" not in dump_str, f"Leak detected: {dump_str}"


def test_security_models_max_depth() -> None:
    class Container(SecureBaseModel):
        payload: object

    # Create depth just above max to trigger the branch in tuples/sets
    payload: object = "value"
    for _ in range(105):
        payload = {"a": payload}
    model = Container(payload=payload)
    dumped = model.model_dump()
    dump_str = str(dumped)
    assert "MAX_DEPTH_REACHED" in dump_str


def test_security_models_max_depth_collections() -> None:
    class Container(SecureBaseModel):
        payload: object

    # Create depth just above max to trigger the branch in tuples/sets
    payload_list: object = "value"
    for _ in range(105):
        payload_list = [payload_list]

    payload_tuple: object = "value"
    for _ in range(105):
        payload_tuple = (payload_tuple,)

    # We can't nest sets because sets elements must be hashable,
    # but we can do a mix of tuples and frozensets or we just do max depth lists and dicts.

    model = Container(payload=payload_list)
    dumped = model.model_dump()
    dump_str = str(dumped)
    assert "MAX_DEPTH_REACHED" in dump_str

    model2 = Container(payload=payload_tuple)
    dumped2 = model2.model_dump()
    dump_str2 = str(dumped2)
    assert "MAX_DEPTH_REACHED" in dump_str2
