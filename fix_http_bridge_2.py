import re

with open("src/taipanstack/bridges/http_bridge.py", "r") as f:
    content = f.read()

# Replace HttpxRequestKwargs block
new_block = """    class HttpxRequestKwargs(TypedDict, total=False):
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
    # Runtime fallback
    HttpxClientKwargs = dict
    HttpxRequestKwargs = dict
    HttpxSafeRequestKwargs = dict
"""

# replace the block
content = re.sub(
    r"    class HttpxRequestKwargs\(TypedDict, total=False\):.*?else:\n    # Runtime fallback\n    HttpxClientKwargs = dict\n    HttpxRequestKwargs = dict\n",
    new_block,
    content,
    flags=re.DOTALL
)

# Replace safe_request **kwargs to use HttpxSafeRequestKwargs
content = re.sub(
    r"def safe_request\((.*?)\*\*kwargs: Unpack\[HttpxRequestKwargs\]\)",
    r"def safe_request(\1**kwargs: Unpack[HttpxSafeRequestKwargs])",
    content,
    flags=re.DOTALL
)

with open("src/taipanstack/bridges/http_bridge.py", "w") as f:
    f.write(content)

print("Applied HttpxSafeRequestKwargs")
