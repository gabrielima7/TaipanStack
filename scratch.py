from taipanstack.security.jwt import encode_jwt

result = encode_jwt({"payload": 1}, 123, algorithm="HS256")
print(result)
