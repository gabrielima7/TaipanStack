import httpx
from typing import TypedDict, Unpack, TYPE_CHECKING
import typing

if TYPE_CHECKING:
    from typing import Mapping, Sequence, IO, Callable
    class RequestKwargs(TypedDict, total=False):
        content: str | bytes | typing.Iterable[bytes] | typing.AsyncIterable[bytes] | None
        data: typing.Mapping[str, typing.Any] | None
        files: typing.Mapping[str, typing.IO[bytes] | bytes | str | tuple[str | None, typing.IO[bytes] | bytes | str] | tuple[str | None, typing.IO[bytes] | bytes | str, str | None] | tuple[str | None, typing.IO[bytes] | bytes | str, str | None, typing.Mapping[str, str]]] | typing.Sequence[tuple[str, typing.IO[bytes] | bytes | str | tuple[str | None, typing.IO[bytes] | bytes | str] | tuple[str | None, typing.IO[bytes] | bytes | str, str | None] | tuple[str | None, typing.IO[bytes] | bytes | str, str | None, typing.Mapping[str, str]]]] | None
        json: typing.Any | None
        params: httpx.QueryParams | typing.Mapping[str, str | int | float | bool | None | typing.Sequence[str | int | float | bool | None]] | list[tuple[str, str | int | float | bool | None]] | tuple[tuple[str, str | int | float | bool | None], ...] | str | bytes | None
        headers: httpx.Headers | typing.Mapping[str, str] | typing.Mapping[bytes, bytes] | typing.Sequence[tuple[str, str]] | typing.Sequence[tuple[bytes, bytes]] | None
        cookies: httpx.Cookies | dict[str, str] | list[tuple[str, str]] | None
        auth: tuple[str | bytes, str | bytes] | typing.Callable[[httpx.Request], httpx.Request] | httpx.Auth | None
        follow_redirects: bool
        timeout: float | tuple[float | None, float | None, float | None, float | None] | httpx.Timeout | None

async def foo(**kwargs: Unpack[RequestKwargs]) -> None:
    async with httpx.AsyncClient() as client:
        await client.request("GET", "http://example.com", **kwargs)
