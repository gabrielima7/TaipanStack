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
        follow_redirects: bool
        limits: httpx.Limits
        max_redirects: int
        event_hooks: Mapping[str, list[Callable[..., Awaitable[None]]]]
        base_url: httpx.URL | str
        transport: httpx.AsyncBaseTransport
        app: Callable[..., object]
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
# Need to make sure `timeout` is completely removed from `HttpxSafeRequestKwargs` and `HttpxClientKwargs`.
# Wait, for `HttpxClientKwargs`, `SafeHttpClient.__init__` has:
# `self._client_kwargs.setdefault("timeout", 10.0)`
# And `self._client_kwargs` is `client_kwargs`, which does not explicitly have `timeout` in the init signature!
# wait, `SafeHttpClient.__init__` signature is:
# def __init__(self, *, ssrf_protection: bool = True, retry_config: RetryConfig | None = None, circuit_breaker: CircuitBreaker | None = None, retryable_status_codes: frozenset[int] = _RETRYABLE_STATUS_CODES, **client_kwargs: Unpack[HttpxClientKwargs]) -> None:
# Then it passes `self._client_kwargs` to `httpx.AsyncClient(**self._client_kwargs)`. But it does:
# `timeout = self._client_kwargs.pop("timeout", 10.0)`
# `self._client = httpx.AsyncClient(timeout=timeout, **self._client_kwargs)`
# So `self._client_kwargs` MUST NOT contain `timeout` when passed to `httpx.AsyncClient`!
# BUT `timeout` can be passed to `__init__`! If it's passed to `__init__`, and `HttpxClientKwargs` doesn't have `timeout`, mypy will complain if we try to pass `timeout=5.0` to `SafeHttpClient`.
# Actually, if we define `timeout: httpx._types.TimeoutTypes` in `HttpxClientKwargs`, but then unpack it into `httpx.AsyncClient(timeout=timeout, **self._client_kwargs)`, mypy will say "AsyncClient gets multiple values for keyword argument 'timeout'".
# Because `**self._client_kwargs` still has the type `Unpack[HttpxClientKwargs]`!
# Since `dict.pop` doesn't change the static type of `self._client_kwargs`, passing it as `**self._client_kwargs` will still make mypy think `timeout` might be in it!
# SOLUTION: cast `self._client_kwargs` before unpacking it? Or just don't pass explicit `timeout` to `httpx.AsyncClient`, but instead let `httpx.AsyncClient(**self._client_kwargs)` receive `timeout`!
# Wait! `httpx.AsyncClient` accepts `timeout` in `**kwargs`? No, it has `timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG` as a keyword argument.
# So `httpx.AsyncClient(**self._client_kwargs)` is fine IF `timeout` is in `self._client_kwargs`.
# So instead of `timeout = self._client_kwargs.pop("timeout", 10.0); self._client = httpx.AsyncClient(timeout=timeout, **self._client_kwargs)`, we can just do:
# `self._client_kwargs.setdefault("timeout", 10.0); self._client = httpx.AsyncClient(**self._client_kwargs)`.
# Let's fix that too.

# Fix __aenter__ pop
content = content.replace(
    'timeout = self._client_kwargs.pop("timeout", 10.0)\n        self._client = httpx.AsyncClient(\n            timeout=timeout,\n            **self._client_kwargs,\n        )',
    'self._client = httpx.AsyncClient(**self._client_kwargs)'
)

# And add `timeout` back to `HttpxClientKwargs`:
content = content.replace(
    "mounts: Mapping[str, httpx.AsyncBaseTransport | None]\n        follow_redirects: bool",
    "mounts: Mapping[str, httpx.AsyncBaseTransport | None]\n        timeout: httpx._types.TimeoutTypes\n        follow_redirects: bool"
)

with open("src/taipanstack/bridges/http_bridge.py", "w") as f:
    f.write(content)
