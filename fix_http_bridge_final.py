import re

with open("src/taipanstack/bridges/http_bridge.py", "r") as f:
    content = f.read()

# Replace TYPE_CHECKING and Any
content = content.replace("from typing import TYPE_CHECKING, Any", "from typing import TYPE_CHECKING, TypedDict, Unpack")

type_checking_block = """if TYPE_CHECKING:
    import httpx
    from httpx._types import (
        AuthTypes, CookieTypes, HeaderTypes, QueryParamTypes,
        RequestContent, RequestData, RequestFiles, TimeoutTypes,
        CertTypes, ProxyTypes
    )

    class HttpxClientKwargs(TypedDict, total=False):
        auth: AuthTypes
        params: QueryParamTypes
        headers: HeaderTypes
        cookies: CookieTypes
        verify: httpx._types.VerifyTypes | str | bool
        cert: CertTypes
        http1: bool
        http2: bool
        proxies: ProxyTypes
        mounts: dict[str, httpx.AsyncBaseTransport | None]
        timeout: TimeoutTypes
        follow_redirects: bool
        limits: httpx.Limits
        max_redirects: int
        event_hooks: dict[str, list[Callable[..., Awaitable[None]]]]
        base_url: httpx.URL | str
        transport: httpx.AsyncBaseTransport
        app: Callable[..., object]
        trust_env: bool
        default_encoding: str

    class HttpxRequestKwargs(TypedDict, total=False):
        content: RequestContent
        data: RequestData
        files: RequestFiles
        json: object
        params: QueryParamTypes
        headers: HeaderTypes
        cookies: CookieTypes
        auth: AuthTypes
        follow_redirects: bool
        timeout: TimeoutTypes
        extensions: dict[str, object]

    class HttpxSafeRequestKwargs(TypedDict, total=False):
        content: RequestContent
        data: RequestData
        files: RequestFiles
        json: object
        params: QueryParamTypes
        headers: HeaderTypes
        cookies: CookieTypes
        auth: AuthTypes
        follow_redirects: bool
        extensions: dict[str, object]
else:
    HttpxClientKwargs = dict  # type: ignore[misc]
    HttpxRequestKwargs = dict  # type: ignore[misc]
    HttpxSafeRequestKwargs = dict  # type: ignore[misc]
"""

# Insert type checking block right after imports
if "from taipanstack.resilience.retry import RetryConfig, calculate_delay" in content:
    content = content.replace(
        "from taipanstack.resilience.retry import RetryConfig, calculate_delay",
        "from taipanstack.resilience.retry import RetryConfig, calculate_delay\n" + type_checking_block
    )

# Use Unpack
content = re.sub(
    r"def safe_request\((.*?)\*\*kwargs: Any\)",
    r"def safe_request(\1**kwargs: Unpack[HttpxSafeRequestKwargs])",
    content,
    flags=re.DOTALL
)

content = content.replace("**kwargs: Any", "**kwargs: Unpack[HttpxRequestKwargs]")
content = content.replace("**kw: Any", "**kw: Unpack[HttpxRequestKwargs]")
content = content.replace("**client_kwargs: Any", "**client_kwargs: Unpack[HttpxClientKwargs]")

with open("src/taipanstack/bridges/http_bridge.py", "w") as f:
    f.write(content)
