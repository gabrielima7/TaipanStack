import timeit
import unicodedata
import re
import sys

def original(result):
    return "".join(
        c for c in result if unicodedata.category(c) != "Cc" or c in "\n\r\t"
    )

# Pre-compute control char translation table for all unicode control chars (Cc)
_CONTROL_CHARS = {i: None for i in range(sys.maxunicode) if unicodedata.category(chr(i)) == 'Cc' and chr(i) not in '\n\r\t'}

def optimized_translate(result):
    return result.translate(_CONTROL_CHARS)

# Also regex
_CC_REGEX = re.compile(r'[\x00-\x08\x0b\x0c\x0e\x0f-\x1f\x7f-\x9f]')

def optimized_regex(result):
    return _CC_REGEX.sub('', result)

test_string = "Hello, World! This is a normal string.\n\r\t\x00\x01\x02\x03\x04" * 10

print("original", timeit.timeit(lambda: original(test_string), number=10000))
print("translate", timeit.timeit(lambda: optimized_translate(test_string), number=10000))
print("regex", timeit.timeit(lambda: optimized_regex(test_string), number=10000))
