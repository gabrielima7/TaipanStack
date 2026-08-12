with open('tests/test_fuzz_guard_env_variable_empty.py', 'r') as f:
    content = f.read()
content = content.replace('Exception', 'ValueError, TypeError, Exception')
with open('tests/test_fuzz_guard_env_variable_empty.py', 'w') as f:
    f.write(content)
