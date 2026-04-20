with open("tests/test_ultra_final_operations_expected.py", "r") as f:
    content = f.read()

content = content.replace("test_func()", "test_ultra_final_func_expected()")

with open("tests/test_ultra_final_operations_expected.py", "w") as f:
    f.write(content)
