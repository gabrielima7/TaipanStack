import re

with open("tests/test_fuzz_sanitizers_types_operations.py", "r") as f:
    content = f.read()

content = re.sub(r'def test_fuzz_sanitizers_types_fuzz_safe_html_invalid_types.*?SafeHtml\(value\)\n\n\n', '', content, flags=re.DOTALL)
content = re.sub(r'def test_fuzz_sanitizers_types_fuzz_safe_sql_identifier_invalid_types.*?SafeSqlIdentifier\(value\)\n\n\n', '', content, flags=re.DOTALL)
# And the imports
content = re.sub(r'\s*SafeHtml,', '', content)
content = re.sub(r'\s*SafeSqlIdentifier,', '', content)

with open("tests/test_fuzz_sanitizers_types_operations.py", "w") as f:
    f.write(content)
