"""Chaos testing for subprocess robustness."""

from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.utils.subprocess import _filter_environment, run_safe_command


@given(
    env=st.dictionaries(
        keys=st.text(min_size=1, max_size=1000),
        values=st.text(min_size=0, max_size=10000),
    ),
    allowed=st.lists(st.text(min_size=1, max_size=1000), max_size=10),
)
@settings(max_examples=100, deadline=None)
def test_chaos_subprocess_filter_environment_fuzzing(
    env: dict[str, str], allowed: list[str]
) -> None:
    """Fuzz _filter_environment with extreme strings."""
    filtered = _filter_environment(env, allowed_env_vars=allowed)

    # Verify no unallowed keys leak through
    allowed_upper = {k.upper() for k in allowed}
    for k in filtered:
        assert k.upper() in allowed_upper


@given(
    env=st.dictionaries(
        keys=st.text(alphabet=st.characters(blacklist_categories=("Cs",)), min_size=1, max_size=100),
        values=st.text(alphabet=st.characters(blacklist_categories=("Cs",)), min_size=0, max_size=1000),
    ),
    allowed=st.lists(
        st.text(alphabet=st.characters(blacklist_categories=("Cs",)), min_size=1, max_size=100),
        max_size=5,
    ),
)
@settings(max_examples=50, deadline=None)
def test_chaos_subprocess_run_safe_command_env_fuzzing(
    env: dict[str, str], allowed: list[str]
) -> None:
    """Fuzz run_safe_command environment filtering."""
    # We use dry_run to bypass actual subprocess execution while testing the filtering logic
    result = run_safe_command(
        ["echo", "test"],
        env=env,
        allowed_env_vars=allowed,
        dry_run=True,
    )
    assert result.success
    assert "[DRY-RUN]" in result.stdout
