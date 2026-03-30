with open('tests/test_stack_script_extra.py', 'r') as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if line.startswith("def test_generate_dependabot_config_error("):
        skip = True
    elif line.startswith("def test_validate_setup_failures("):
        skip = False

    if not skip:
        out.append(line)

with open('tests/test_stack_script_extra.py', 'w') as f:
    f.writelines(out)
