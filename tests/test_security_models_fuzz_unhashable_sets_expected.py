from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.security.models import _mask_data


class UnhashableDict(dict):
    def __hash__(self):
        return 1

    def __eq__(self, other):
        return False


@given(st.dictionaries(st.text(), st.text()))
@settings(max_examples=50)
def test_fuzz_mask_data_unhashable_sets_expected(d):
    data = {UnhashableDict(d)}
    result = _mask_data(data)
    assert isinstance(result, list)


def test_fuzz_mask_data_unhashable_sets_multiple_expected():
    data = {UnhashableDict({"a": "b"}), UnhashableDict({"c": "d"})}
    result = _mask_data(data)
    assert isinstance(result, list)
    assert len(result) == 2
