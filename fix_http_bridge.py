import re

with open("src/taipanstack/bridges/http_bridge.py", "r") as f:
    content = f.read()

# Remove Any
content = content.replace("from typing import TYPE_CHECKING, Any", "from typing import TYPE_CHECKING, TypedDict, Unpack")

# Add the TypedDicts under TYPE_CHECKING
type_checking_block = """if TYPE_CHECKING:
    import httpx
    from httpx._types import (
        AuthTypes, CookieTypes, HeaderTypes, QueryParamTypes,
        RequestContent, RequestData, RequestFiles, TimeoutTypes,
        VerifyTypes, CertTypes, ProxiesTypes
    )

    class HttpxClientKwargs(TypedDict, total=False):
        auth: AuthTypes
        params: QueryParamTypes
        headers: HeaderTypes
        cookies: CookieTypes
        verify: VerifyTypes
        cert: CertTypes
        http1: bool
        http2: bool
        proxies: ProxiesTypes
        mounts: dict[str, httpx.AsyncBaseTransport | None]
        timeout: TimeoutTypes
        follow_redirects: bool
        limits: httpx.Limits
        max_redirects: int
        event_hooks: dict[str, list[typing.Callable[..., typing.Awaitable[None]]]]
        base_url: httpx.URL | str
        transport: httpx.AsyncBaseTransport
        app: typing.Callable[..., typing.Any]
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
else:
    # Runtime fallback
    HttpxClientKwargs = dict
    HttpxRequestKwargs = dict
"""

# Find TYPE_CHECKING block or add it
if "if TYPE_CHECKING:\n    import httpx" in content:
    content = content.replace("if TYPE_CHECKING:\n    import httpx\n", type_checking_block)
else:
    # Just insert it after imports
    content = content.replace(
        "from taipanstack.resilience.retry import RetryConfig, calculate_delay",
        "from taipanstack.resilience.retry import RetryConfig, calculate_delay\nimport typing\n" + type_checking_block
    )

# Now, wait! The TypedDict above uses typing.Any for app event_hooks. Let's fix that.
# Remove typing.Any and just use `object`.
type_checking_block = type_checking_block.replace("typing.Any", "object")
content = content.replace("typing.Any", "object")

# Replace **kwargs: Any with **kwargs: Unpack[HttpxRequestKwargs]
content = content.replace("**kwargs: Any", "**kwargs: Unpack[HttpxRequestKwargs]")
content = content.replace("**kw: Any", "**kw: Unpack[HttpxRequestKwargs]")
content = content.replace("**client_kwargs: Any", "**client_kwargs: Unpack[HttpxClientKwargs]")

# The previous error "Overlap between argument names and ** TypedDict items: "timeout""
# Need to remove timeout from HttpxRequestKwargs since safe_request has timeout explicit.
content = content.replace("        timeout: TimeoutTypes\n", "")
# Wait, safe_request has timeout explicitly, but SafeHttpClient.request does NOT have timeout explicitly.
# Wait, SafeHttpClient.request just passes **kwargs to httpx!
# Let's check SafeHttpClient.request signature: `async def request(self, method: str, url: str, **kwargs: Unpack[HttpxRequestKwargs])`
# If we remove `timeout` from `HttpxRequestKwargs`, we can't pass `timeout` to `SafeHttpClient.request`.
# Why did mypy complain about overlap? "Overlap between argument names and ** TypedDict items: "timeout"" on line 199.
# safe_request signature:
# async def safe_request(method: str, url: str, *, ..., timeout: float | None = 10.0, **kwargs: Unpack[HttpxRequestKwargs])
# MyPy complains because both `safe_request` and `HttpxRequestKwargs` have `timeout`.
# How to solve this?
# We can create a separate TypedDict for safe_request which doesn't have `timeout`, or just remove `timeout` from `safe_request` signature and use kwargs? No, safe_request has explicit `timeout` parameter.
# We can use `HttpxSafeRequestKwargs` without `timeout` for `safe_request`, and `HttpxRequestKwargs` with `timeout` for `SafeHttpClient.request`.

with open("src/taipanstack/bridges/http_bridge.py", "w") as f:
    f.write(content)

print("Modified script generated.")
