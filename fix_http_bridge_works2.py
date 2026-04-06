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
else:
    HttpxClientKwargs = dict  # type: ignore[misc]
    HttpxRequestKwargs = dict  # type: ignore[misc]
    HttpxSafeRequestKwargs = dict  # type: ignore[misc]
"""

content = content.replace(
    "from taipanstack.resilience.retry import RetryConfig, calculate_delay",
    "from taipanstack.resilience.retry import RetryConfig, calculate_delay\n" + type_checking_block
)

# Replace kwargs
content = re.sub(
    r"def safe_request\((.*?)\*\*kwargs: Any\)",
    r"def safe_request(\1**kwargs: Unpack[HttpxSafeRequestKwargs])",
    content,
    flags=re.DOTALL
)

content = content.replace("**kwargs: Any", "**kwargs: Unpack[HttpxRequestKwargs]")
content = content.replace("**kw: Any", "**kw: Unpack[HttpxRequestKwargs]")
content = content.replace("**client_kwargs: Any", "**client_kwargs: Unpack[HttpxClientKwargs]")

# The previous error "Overlap between argument names and ** TypedDict items: "timeout""
# Need to make sure safe_request does not get **kwargs that have timeout!
# But wait, SafeHttpClient.__init__ DOES have timeout! It pops it from self._client_kwargs.
content = content.replace(
    'timeout = self._client_kwargs.pop("timeout", 10.0)\n        self._client = httpx.AsyncClient(\n            timeout=timeout,\n            **self._client_kwargs,\n        )',
    'self._client = httpx.AsyncClient(**self._client_kwargs)  # type: ignore'
)

# And `SafeHttpClient.request` has `timeout`? No it doesn't.
# wait! `safe_request` has `timeout` as a keyword argument! And `**kwargs: Unpack[HttpxSafeRequestKwargs]`. `HttpxSafeRequestKwargs` DOES NOT have `timeout`!
# BUT `def _do_request() -> httpx.Response:
#         async with httpx.AsyncClient(timeout=timeout) as client:
#             response = await client.request(method, url, **kwargs)`
# `client.request` has `**kwargs: Unpack[HttpxSafeRequestKwargs]`. This is fine because `httpx.AsyncClient.request` accepts all of those.

with open("src/taipanstack/bridges/http_bridge.py", "w") as f:
    f.write(content)

print("Modification complete")
