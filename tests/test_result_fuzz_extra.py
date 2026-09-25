from hypothesis import given
from hypothesis import strategies as st

from taipanstack.core.result import Err, Ok, collect_results


# Generate random results: either Ok with an integer or Err with a ValueError
@st.composite
def results_strategy(draw):
    is_ok = draw(st.booleans())
    if is_ok:
        return Ok(draw(st.integers()))
    else:
        return Err(ValueError(draw(st.text())))


@given(st.lists(results_strategy()))
def test_collect_results_properties(results_list):
    """
    Property-based test for `collect_results`.

    Properties:
    1. If all elements in the input list are Ok, the result must be Ok and
       contain a list of all the values in the same order.
    2. If there is at least one Err in the input list, the result must be Err
       and should match the *first* Err encountered in the input.
    """
    out = collect_results(results_list)

    has_err = any(isinstance(r, Err) for r in results_list)

    if has_err:
        assert isinstance(out, Err)
        # Find the first Err in the input list
        first_err = next(r for r in results_list if isinstance(r, Err))
        assert out.err_value == first_err.err_value
    else:
        assert isinstance(out, Ok)
        # Verify the unwrapped list matches the ok values
        expected_values = [r.ok_value for r in results_list]
        assert out.ok_value == expected_values
