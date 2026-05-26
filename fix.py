with open('src/taipanstack/bridges/db_bridge.py', 'r') as f:
    content = f.read()

content = content.replace(
    '''if TYPE_CHECKING:
    import redis.asyncio as aioredis
    from sqlalchemy.ext.asyncio import AsyncEngine''',
    '''if TYPE_CHECKING:
    import redis.asyncio as aioredis  # type: ignore[import-untyped, import-not-found]
    from sqlalchemy.ext.asyncio import AsyncEngine  # type: ignore[import-untyped, import-not-found]'''
)

with open('src/taipanstack/bridges/db_bridge.py', 'w') as f:
    f.write(content)
