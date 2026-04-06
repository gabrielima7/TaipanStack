import re

with open("src/taipanstack/bridges/http_bridge.py", "r") as f:
    content = f.read()

# Replace TYPE_CHECKING and Any
content = content.replace("from typing import TYPE_CHECKING, Any", "from typing import TYPE_CHECKING, TypedDict, Unpack, Mapping")

type_checking_block = """if TYPE_CHECKING:
    import ssl
    import httpx

    class HttpxClientKwargs(TypedDict, total=False):
        auth: httpx._types.AuthTypes
        params: httpx._types.QueryParamTypes
        headers: httpx._types.HeaderTypes
        cookies: httpx._types.CookieTypes
        verify: ssl.SSLContext | str | bool
        cert: httpx._types.CertTypes
        http1: bool
        http2: bool
        proxy: httpx._types.ProxyTypes
        proxies: httpx._types.ProxyTypes
        mounts: Mapping[str, httpx.AsyncBaseTransport | None]
        timeout: httpx._types.TimeoutTypes
        follow_redirects: bool
        limits: httpx.Limits
        max_redirects: int
        event_hooks: Mapping[str, list[Callable[..., Awaitable[None]]]]
        base_url: httpx.URL | str
        transport: httpx.AsyncBaseTransport
        trust_env: bool
        default_encoding: str

    class HttpxRequestKwargs(TypedDict, total=False):
        content: httpx._types.RequestContent
        data: httpx._types.RequestData
        files: httpx._types.RequestFiles
        json: object
        params: httpx._types.QueryParamTypes
        headers: httpx._types.HeaderTypes
        cookies: httpx._types.CookieTypes
        auth: httpx._types.AuthTypes
        follow_redirects: bool
        timeout: httpx._types.TimeoutTypes
        extensions: Mapping[str, object]

    class HttpxSafeRequestKwargs(TypedDict, total=False):
        content: httpx._types.RequestContent
        data: httpx._types.RequestData
        files: httpx._types.RequestFiles
        json: object
        params: httpx._types.QueryParamTypes
        headers: httpx._types.HeaderTypes
        cookies: httpx._types.CookieTypes
        auth: httpx._types.AuthTypes
        follow_redirects: bool
        extensions: Mapping[str, object]
"""

content = content.replace(
    "from taipanstack.resilience.retry import RetryConfig, calculate_delay",
    "from taipanstack.resilience.retry import RetryConfig, calculate_delay\n" + type_checking_block
)

# Fix __aenter__ pop
content = content.replace(
    'timeout = self._client_kwargs.pop("timeout", 10.0)\n        self._client = httpx.AsyncClient(\n            timeout=timeout,\n            **self._client_kwargs,\n        )',
    'self._client = httpx.AsyncClient(**self._client_kwargs)'  # type: ignore[arg-type]
)
# Add type ignore to that specific line in python code:
content = content.replace('self._client = httpx.AsyncClient(**self._client_kwargs)', 'self._client = httpx.AsyncClient(**self._client_kwargs)  # type: ignore[arg-type]')

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
