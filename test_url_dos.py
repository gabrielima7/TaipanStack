from taipanstack.security.validators import validate_url

try:
    print(validate_url("http://" + "a" * 2000 + ".com"))
except Exception as e:
    print(e)
