import contextlib

import hypothesis.strategies as st
from hypothesis import given, settings

from taipanstack.security.jwt import decode_jwt


@settings(max_examples=200)
@given(
    st.text(),
    st.text(),
    st.lists(
        st.one_of(
            st.text(),
            st.integers(),
            st.floats(),
            st.booleans(),
            st.none(),
            st.lists(st.text()),
            st.dictionaries(st.text(), st.text()),
        )
    ),
    st.text(),
)
def test_fuzz_jwt_decode_malformed_algs(token, secret, algs, aud):
    with contextlib.suppress(TypeError, ValueError):
        decode_jwt(token, secret, algorithms=algs, audience=aud)
