import math

from taipanstack.utils.rate_limit import RateLimiter


def test_chaos_rate_limit_tokens_mutation_rate_limit_survives_type_mutation_tokens_arg_expected() -> (
    None
):
    limiter = RateLimiter(10, 10.0)

    # Should safely fail closed when given invalid token types
    assert limiter.consume("string") is False  # type: ignore
    assert limiter.consume(None) is False  # type: ignore
    assert limiter.consume(object()) is False  # type: ignore

    # Should safely fail closed when given nan
    assert limiter.consume(math.nan) is False
