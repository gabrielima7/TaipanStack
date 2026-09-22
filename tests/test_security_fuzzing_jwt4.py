
import contextlib

import hypothesis.strategies as st
from hypothesis import given, settings

from taipanstack.security.jwt import decode_jwt


@settings(max_examples=100)
@given(
    st.text(alphabet=st.characters(exclude_characters=set("noneNONE"))),
)
def test_fuzz_jwt_decode_none_algs(alg):
    with contextlib.suppress(TypeError, ValueError):
        decode_jwt("token", "secret", algorithms=["HS256", alg], audience="app")
