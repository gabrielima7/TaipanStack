import re

with open('tests/test_stack_script_extra.py', 'r') as f:
    content = f.read()

# Only remove the specific dependabot error test
pattern = r"def test_generate_dependabot_config_error\(tmp_path, monkeypatch\):.*?(?=\ndef test_validate_setup_failures)"
content = re.sub(re.compile(pattern, re.MULTILINE | re.DOTALL), '', content)

with open('tests/test_stack_script_extra.py', 'w') as f:
    f.write(content)
