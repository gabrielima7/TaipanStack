import asyncio
import time
from pathlib import Path

import pytest
from result import Err, Ok

from taipanstack.core.result import collect_results, map_async, safe, safe_from
from taipanstack.resilience.circuit_breaker import CircuitBreakerError, circuit_breaker
from taipanstack.resilience.retry import RetryConfig, RetryError, calculate_delay, retry
from taipanstack.security.password import hash_password, verify_password
from taipanstack.security.sanitizers import (
    sanitize_env_value,
    sanitize_filename,
    sanitize_path,
    sanitize_sql_identifier,
    sanitize_string,
)
from taipanstack.security.validators import (
    validate_email,
    validate_project_name,
    validate_python_version,
    validate_url,
)
from taipanstack.utils.cache import cached
from taipanstack.utils.context import correlation_scope, get_correlation_id, set_correlation_id
from taipanstack.utils.rate_limit import RateLimitError, rate_limit


def test_validators_happy_and_error_paths():
    assert validate_email("a@b.com") == "a@b.com"
    assert validate_project_name("proj_1") == "proj_1"
    assert validate_python_version("3.11") == "3.11"
    assert validate_url("https://example.com") == "https://example.com"
    with pytest.raises(ValueError):
        validate_email("nope")
    with pytest.raises(ValueError):
        validate_project_name("../bad")
    with pytest.raises(ValueError):
        validate_python_version("3")
    with pytest.raises(ValueError):
        validate_url("ftp://example.com", allowed_schemes=("https",))


def test_sanitizers_cover_string_path_filename_and_env(tmp_path: Path):
    assert sanitize_string(" <b>x</b> ", allow_html=False) == "x"
    assert sanitize_filename("../../a?.txt") == "a.txt"
    clean = sanitize_path("a/../b", base_dir=tmp_path)
    assert str(clean).endswith("b")
    assert sanitize_sql_identifier("users;drop") == "usersdrop"
    assert sanitize_env_value("A\nB", allow_multiline=False) == "A B"


def test_password_hash_and_verify_roundtrip():
    pw = "StrongPassword!123"
    hashed = hash_password(pw)
    assert hashed != pw
    assert verify_password(pw, hashed)
    assert not verify_password("wrong", hashed)


def test_result_helpers_sync_and_async():
    @safe
    def divide(a: int, b: int) -> float:
        return a / b

    ok = divide(8, 2)
    err = divide(1, 0)
    assert isinstance(ok, Ok)
    assert isinstance(err, Err)
    assert collect_results([Ok(1), Ok(2)]).ok_value == [1, 2]

    async def add1(v: int) -> int:
        return v + 1

    mapped = asyncio.run(map_async(Ok(2), add1))
    assert mapped.ok_value == 3

    @safe_from(ValueError)
    def parse_int(v: str) -> int:
        return int(v)

    assert isinstance(parse_int("2"), Ok)
    assert isinstance(parse_int("x"), Err)


def test_cache_and_rate_limit_decorators():
    calls = {"n": 0}

    @cached(ttl=60.0)
    def compute(x: int):
        calls["n"] += 1
        return Ok(x * 2)

    assert compute(3).ok_value == 6
    assert compute(3).ok_value == 6
    assert calls["n"] == 1

    @rate_limit(max_calls=2, time_window=10.0)
    def limited() -> str:
        return "ok"

    assert limited().ok_value == "ok"
    assert limited().ok_value == "ok"
    limited_result = limited()
    assert isinstance(limited_result, Err)
    assert isinstance(limited_result.err_value, RateLimitError)


def test_retry_delay_and_exhaustion_behavior(monkeypatch: pytest.MonkeyPatch):
    d = calculate_delay(2, RetryConfig(max_attempts=3))
    assert d >= 0

    monkeypatch.setattr(time, "sleep", lambda *_: None)
    count = {"n": 0}

    @retry(max_attempts=2, initial_delay=0, jitter=False, on=(ValueError,))
    def flaky() -> None:
        count["n"] += 1
        raise ValueError("boom")

    with pytest.raises(RetryError):
        flaky()
    assert count["n"] == 2


def test_circuit_breaker_opens_and_blocks_calls(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(time, "sleep", lambda *_: None)
    count = {"n": 0}

    @circuit_breaker(failure_threshold=2, timeout=30)
    def sometimes_fail() -> str:
        count["n"] += 1
        raise ValueError("x")

    with pytest.raises(ValueError):
        sometimes_fail()
    with pytest.raises(ValueError):
        sometimes_fail()
    with pytest.raises(CircuitBreakerError):
        sometimes_fail()
    assert count["n"] == 2


def test_request_context_roundtrip():
    set_correlation_id("abc")
    assert get_correlation_id() == "abc"
    with correlation_scope("xyz"):
        assert get_correlation_id() == "xyz"
    assert get_correlation_id() == "abc"
