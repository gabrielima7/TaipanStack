from taipanstack.resilience.resilience import timeout


def test_resilience_chaos_timeout_corrupt_float_expected() -> None:
    class CorruptFloat(float):
        def __ge__(self, other: object) -> bool:
            raise RuntimeError("Chaos __ge__")

        def __add__(self, other: object) -> float:
            raise RuntimeError("Chaos __add__")

        def __mul__(self, other: object) -> float:
            raise RuntimeError("Chaos __mul__")

        def __lt__(self, other: object) -> bool:
            raise RuntimeError("Chaos __lt__")

    @timeout(CorruptFloat(1.0))
    def my_func() -> int:
        return 1

    result = my_func()
    # Verify it returns an Err because validation failed
    assert result.is_err()
