import contextlib

import hypothesis.strategies as st
from hypothesis import given, settings

from taipanstack.security.jwt import encode_jwt


@settings(max_examples=200)
@given(
    st.one_of(
        st.integers(),
        st.floats(),
        st.booleans(),
        st.none(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.integers()),
    ),
    st.text(),
    st.text(),
)
def test_fuzz_jwt_encode_malformed_payload(payload, secret, alg):
    with contextlib.suppress(TypeError, ValueError):
        encode_jwt(payload, secret, algorithm=alg)

@settings(max_examples=200)
@given(
    st.text(),
    st.one_of(
        st.integers(),
        st.floats(),
        st.booleans(),
        st.none(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    ),
    st.text(),
)
def test_fuzz_jwt_encode_malformed_secret(payload, secret, alg):
    with contextlib.suppress(TypeError, ValueError):
        encode_jwt({"test": "data"}, secret, algorithm=alg)

@settings(max_examples=200)
@given(
    st.text(),
    st.text(),
    st.one_of(
        st.integers(),
        st.floats(),
        st.booleans(),
        st.none(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    ),
)
def test_fuzz_jwt_encode_malformed_alg(payload, secret, alg):
    with contextlib.suppress(TypeError, ValueError):
        encode_jwt({"test": "data"}, "secret", algorithm=alg)
