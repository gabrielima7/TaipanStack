from taipanstack.security.models import SecureBaseModel

class TestModel(SecureBaseModel):
    token: str

m = TestModel(token="secret_token")
print(m.model_dump())
print(m.model_dump_json())
