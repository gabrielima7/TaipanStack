from taipanstack.security.validators import validate_python_version

try:
    print(validate_python_version("3.12"))
    print(validate_python_version("3.000000000000000000000010"))
except Exception as e:
    print(e)
