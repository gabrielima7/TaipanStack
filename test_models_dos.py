import json
from pydantic import Field
from taipanstack.security.models import SecureBaseModel

class TestModel(SecureBaseModel):
    data: list

# What if we give it a string inside a list, but max recursion depth is huge?
# Actually, models masking handles lists and dicts and _MAX_RECURSION_DEPTH=100. Let's hit the recursion depth to see if it bypasses correctly.
massive_list = []
current = massive_list
for i in range(150):
    current.append([])
    current = current[0]

m = TestModel(data=massive_list)
res = m.model_dump()
print(res)
