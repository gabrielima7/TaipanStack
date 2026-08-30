from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker


def test_chaos_adaptive_breaker_min_throughput_mutation():
    breaker = AdaptiveCircuitBreaker(min_throughput=5)

    # Simulate corruption of _min_throughput
    breaker._min_throughput = "5"

    # Should safely fail or recover without crashing with TypeError
    breaker.record_failure(ValueError("test"))


def test_chaos_adaptive_breaker_min_throughput_nan_mutation():
    breaker = AdaptiveCircuitBreaker(min_throughput=5)

    # Simulate corruption of _min_throughput to NaN
    breaker._min_throughput = float("nan")

    # Should safely fail or recover without crashing
    breaker.record_failure(ValueError("test"))


def test_chaos_adaptive_breaker_min_throughput_type_error_mutation():
    breaker = AdaptiveCircuitBreaker(min_throughput=5)

    # Simulate corruption of _min_throughput
    class BadInt:
        def __int__(self):
            raise TypeError("test")

    breaker._min_throughput = BadInt()
    breaker.record_failure(ValueError("test"))
