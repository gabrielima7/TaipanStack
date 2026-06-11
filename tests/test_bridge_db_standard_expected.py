"""Tests for the DB Bridge."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import taipanstack.bridges.db_bridge as db_mod
from taipanstack.bridges.db_bridge import ResilientDatabase, ResilientRedis
from taipanstack.core.result import Err, Ok
from taipanstack.resilience.circuit_breaker import CircuitBreaker
from taipanstack.resilience.retry import RetryConfig

# --- helpers ----------------------------------------------------------------


def _setup_sqlalchemy_mock() -> AsyncMock:
    """Create and install an AsyncSession mock on db_mod."""
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=MagicMock())
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    # Install mocks on the module so the code can find them
    db_mod.AsyncSession = MagicMock(return_value=mock_session)  # type: ignore[attr-defined]
    db_mod.sa_text = MagicMock(return_value="SELECT 1")  # type: ignore[attr-defined]

    return mock_session


def _teardown_sqlalchemy_mock() -> None:
    """Remove installed mocks."""
    for attr in ("AsyncSession", "sa_text"):
        if hasattr(db_mod, attr):
            delattr(db_mod, attr)


# --- ResilientDatabase -------------------------------------------------------


class TestResilientDatabase:
    """Tests for the ResilientDatabase wrapper."""

    @pytest.mark.asyncio
    async def test_bridge_db_execute_no_sqlalchemy_expected(self) -> None:
        """Returns Err when SQLAlchemy not installed."""
        db = ResilientDatabase(engine=MagicMock())
        with patch.object(db_mod, "_HAS_SQLALCHEMY", False):
            result = await db.execute("SELECT 1")
        assert isinstance(result, Err)
        assert isinstance(result.err_value, ImportError)

    @pytest.mark.asyncio
    async def test_bridge_db_execute_ok_expected(self) -> None:
        """Successful execution returns Ok."""
        _setup_sqlalchemy_mock()
        try:
            with patch.object(db_mod, "_HAS_SQLALCHEMY", True):
                db = ResilientDatabase(engine=MagicMock())
                result = await db.execute("SELECT 1")

            assert isinstance(result, Ok)
        finally:
            _teardown_sqlalchemy_mock()

    @pytest.mark.asyncio
    async def test_bridge_db_execute_with_circuit_breaker_open_expected(self) -> None:
        """Returns Err when circuit breaker is OPEN."""
        breaker = CircuitBreaker(name="db", failure_threshold=1)
        breaker._record_failure(Exception("fail"))

        with patch.object(db_mod, "_HAS_SQLALCHEMY", True):
            db = ResilientDatabase(engine=MagicMock(), circuit_breaker=breaker)
            result = await db.execute("SELECT 1")

        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_bridge_db_execute_with_retry_expected(self) -> None:
        """Retries on failure then succeeds."""
        mock_result = MagicMock()
        call_count = 0

        async def fake_execute(*a: object, **kw: object) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ConnectionError("temp fail")
            return mock_result

        mock_session = _setup_sqlalchemy_mock()
        mock_session.execute = fake_execute
        try:
            with patch.object(db_mod, "_HAS_SQLALCHEMY", True):
                db = ResilientDatabase(
                    engine=MagicMock(),
                    retry_config=RetryConfig(
                        max_attempts=2, initial_delay=0.01, max_delay=0.02, jitter=False
                    ),
                )
                result = await db.execute("SELECT 1")

            assert isinstance(result, Ok)
        finally:
            _teardown_sqlalchemy_mock()

    @pytest.mark.asyncio
    async def test_bridge_db_execute_all_retries_fail_expected(self) -> None:
        """Returns Err when all retries exhaust."""
        mock_session = _setup_sqlalchemy_mock()
        mock_session.execute = AsyncMock(side_effect=ConnectionError("fail"))

        breaker = CircuitBreaker(name="db_fail", failure_threshold=10)

        try:
            with patch.object(db_mod, "_HAS_SQLALCHEMY", True):
                db = ResilientDatabase(
                    engine=MagicMock(),
                    retry_config=RetryConfig(
                        max_attempts=2, initial_delay=0.01, max_delay=0.02, jitter=False
                    ),
                    circuit_breaker=breaker,
                )
                result = await db.execute("SELECT 1")

            assert isinstance(result, Err)
        finally:
            _teardown_sqlalchemy_mock()

    @pytest.mark.asyncio
    async def test_bridge_db_execute_zero_attempts_returns_runtime_error_expected(
        self,
    ) -> None:
        """A zero-attempt retry config returns the synthetic DB error."""
        _setup_sqlalchemy_mock()
        try:
            with patch.object(db_mod, "_HAS_SQLALCHEMY", True):
                db = ResilientDatabase(
                    engine=MagicMock(),
                    retry_config=RetryConfig(max_attempts=0, jitter=False),
                )
                result = await db.execute("SELECT 1")

            assert isinstance(result, Err)
            assert isinstance(result.err_value, RuntimeError)
            assert str(result.err_value) == "Database execute failed"
        finally:
            _teardown_sqlalchemy_mock()

    @pytest.mark.asyncio
    async def test_bridge_db_health_check_no_sqlalchemy_expected(self) -> None:
        """Health check returns Err without SQLAlchemy."""
        db = ResilientDatabase(engine=MagicMock())
        with patch.object(db_mod, "_HAS_SQLALCHEMY", False):
            result = await db.health_check()
        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_bridge_db_health_check_ok_expected(self) -> None:
        """Health check returns Ok when DB is reachable."""
        _setup_sqlalchemy_mock()
        try:
            with patch.object(db_mod, "_HAS_SQLALCHEMY", True):
                db = ResilientDatabase(engine=MagicMock())
                result = await db.health_check()

            assert isinstance(result, Ok)
            assert result.ok_value is True
        finally:
            _teardown_sqlalchemy_mock()

    @pytest.mark.asyncio
    async def test_bridge_db_health_check_fails_expected(self) -> None:
        """Health check returns Err on DB failure."""
        mock_session = _setup_sqlalchemy_mock()
        mock_session.execute = AsyncMock(side_effect=ConnectionError("db down"))
        try:
            with patch.object(db_mod, "_HAS_SQLALCHEMY", True):
                db = ResilientDatabase(engine=MagicMock())
                result = await db.health_check()

            assert isinstance(result, Err)
        finally:
            _teardown_sqlalchemy_mock()


# --- ResilientRedis -----------------------------------------------------------


class TestResilientRedis:
    """Tests for the ResilientRedis wrapper."""

    @pytest.mark.asyncio
    async def test_bridge_db_execute_no_redis_expected(self) -> None:
        """Returns Err when redis not installed."""
        r = ResilientRedis(client=MagicMock())
        with patch.object(db_mod, "_HAS_REDIS", False):
            result = await r.execute("GET", "key")
        assert isinstance(result, Err)
        assert isinstance(result.err_value, ImportError)

    @pytest.mark.asyncio
    async def test_bridge_db_execute_ok_expected(self) -> None:
        """Successful Redis command returns Ok."""
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=b"value")

        with patch.object(db_mod, "_HAS_REDIS", True):
            r = ResilientRedis(client=mock_client)
            result = await r.execute("GET", "key")

        assert isinstance(result, Ok)
        assert result.ok_value == b"value"

    @pytest.mark.asyncio
    async def test_bridge_db_execute_with_breaker_open_expected(self) -> None:
        """Returns Err when circuit breaker is OPEN."""
        breaker = CircuitBreaker(name="redis", failure_threshold=1)
        breaker._record_failure(Exception("fail"))

        with patch.object(db_mod, "_HAS_REDIS", True):
            r = ResilientRedis(client=MagicMock(), circuit_breaker=breaker)
            result = await r.execute("GET", "key")

        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_bridge_db_execute_failure_records_breaker_expected(self) -> None:
        """Failed command records failure on circuit breaker."""
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(side_effect=ConnectionError("lost"))

        breaker = CircuitBreaker(name="redis_fail", failure_threshold=5)

        with patch.object(db_mod, "_HAS_REDIS", True):
            r = ResilientRedis(client=mock_client, circuit_breaker=breaker)
            result = await r.execute("GET", "key")

        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_bridge_db_execute_failure_without_breaker_returns_err_expected(
        self,
    ) -> None:
        """Failed commands still return Err when no breaker is configured."""
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(side_effect=ConnectionError("lost"))

        with patch.object(db_mod, "_HAS_REDIS", True):
            r = ResilientRedis(client=mock_client)
            result = await r.execute("GET", "key")

        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_bridge_db_health_check_no_redis_expected(self) -> None:
        """Health check returns Err without redis."""
        r = ResilientRedis(client=MagicMock())
        with patch.object(db_mod, "_HAS_REDIS", False):
            result = await r.health_check()
        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_bridge_db_health_check_ok_expected(self) -> None:
        """Health check returns Ok on PONG."""
        mock_client = AsyncMock()
        mock_client.ping = AsyncMock(return_value=True)

        with patch.object(db_mod, "_HAS_REDIS", True):
            r = ResilientRedis(client=mock_client)
            result = await r.health_check()

        assert isinstance(result, Ok)
        assert result.ok_value is True

    @pytest.mark.asyncio
    async def test_bridge_db_health_check_fails_expected(self) -> None:
        """Health check returns Err when Redis is down."""
        mock_client = AsyncMock()
        mock_client.ping = AsyncMock(side_effect=ConnectionError("redis down"))

        with patch.object(db_mod, "_HAS_REDIS", True):
            r = ResilientRedis(client=mock_client)
            result = await r.health_check()

        assert isinstance(result, Err)


def test_bridge_db_db_bridge_import_error_coverage_standard_expected() -> None:
    """Test db_bridge import error fallback branches."""
    import importlib
    import sys

    original_sqlalchemy = sys.modules.pop("sqlalchemy", None)
    original_redis = sys.modules.pop("redis", None)
    sys.modules["sqlalchemy"] = None  # type: ignore
    sys.modules["redis"] = None  # type: ignore
    try:
        import taipanstack.bridges.db_bridge as db_mod

        importlib.reload(db_mod)
        assert db_mod._HAS_SQLALCHEMY is False
        assert db_mod._HAS_REDIS is False
    finally:
        if original_sqlalchemy is not None:
            sys.modules["sqlalchemy"] = original_sqlalchemy
        else:
            sys.modules.pop("sqlalchemy", None)
        if original_redis is not None:
            sys.modules["redis"] = original_redis
        else:
            sys.modules.pop("redis", None)
        importlib.reload(db_mod)


def test_bridge_db_success_coverage_standard_expected():
    import importlib
    import sys
    from unittest.mock import MagicMock

    # Save original modules
    original_db_bridge = sys.modules.get("taipanstack.bridges.db_bridge")

    # Fake successful import
    sys.modules["sqlalchemy"] = MagicMock()
    sys.modules["sqlalchemy.ext"] = MagicMock()
    sys.modules["sqlalchemy.ext.asyncio"] = MagicMock()

    sys.modules["redis"] = MagicMock()
    sys.modules["redis.asyncio"] = MagicMock()

    try:
        from taipanstack.bridges import db_bridge

        importlib.reload(db_bridge)

        assert db_bridge._HAS_SQLALCHEMY is True
        assert db_bridge._HAS_REDIS is True
    finally:
        # Cleanup
        sys.modules.pop("sqlalchemy", None)
        sys.modules.pop("sqlalchemy.ext", None)
        sys.modules.pop("sqlalchemy.ext.asyncio", None)
        sys.modules.pop("redis", None)
        sys.modules.pop("redis.asyncio", None)

        if original_db_bridge:
            sys.modules["taipanstack.bridges.db_bridge"] = original_db_bridge
        importlib.reload(db_bridge)
