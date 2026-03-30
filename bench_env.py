from taipanstack.security.sanitizers import sanitize_env_value
import timeit

large_env = "A" * 4096

def sanitize_env_value_opt(
    value: str,
    *,
    max_length: int = 4096,
    allow_multiline: bool = False,
) -> str:
    if type(value) is not str:
        raise TypeError(f"value must be str, got {type(value).__name__}")

    if not value:
        return ""

    if len(value) <= max_length and "\x00" not in value and (allow_multiline or ("\n" not in value and "\r" not in value)):
        return value

    result = value.replace("\x00", "")
    if not allow_multiline:
        result = result.replace("\n", " ").replace("\r", " ")

    if len(result) > max_length:
        return result[:max_length]
    return result

print(timeit.timeit(lambda: sanitize_env_value(large_env), number=100000))
print(timeit.timeit(lambda: sanitize_env_value_opt(large_env), number=100000))
