from taipanstack.security.validators import validate_email

try:
    print(validate_email("a@b.c"))
    print(validate_email("A" * 65 + "@b.com"))
    print(validate_email("a@" + "b" * 260 + ".com"))
except Exception as e:
    print(e)
