with open("src/taipanstack/bridges/db_bridge.py", "r") as f:
    content = f.read()

type_checking_block = """if TYPE_CHECKING:
    import redis.asyncio as aioredis
    from sqlalchemy.engine import Result as SQLAlchemyResult
    from sqlalchemy.ext.asyncio import AsyncEngine
    from sqlalchemy.sql.executable import Executable"""

protocol_block = """from typing import Any, Coroutine, Generic, Protocol, TypeVar, cast

_T = TypeVar("_T")

class SQLAlchemyResult(Protocol, Generic[_T]):
    pass

class AsyncEngine(Protocol):
    pass

class Executable(Protocol):
    pass

class AsyncSession(Protocol):
    async def execute(self, statement: Executable, **kwargs: object) -> SQLAlchemyResult[object]: ...
    async def __aenter__(self) -> 'AsyncSession': ...
    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None: ...

class aioredis:
    class Redis(Protocol, Generic[_T]): ...
"""

content = content.replace("from typing import TYPE_CHECKING", "from typing import TYPE_CHECKING, Any, Coroutine, Generic, Protocol, TypeVar, cast")
content = content.replace(type_checking_block, protocol_block)

with open("src/taipanstack/bridges/db_bridge.py", "w") as f:
    f.write(content)
