import time
from taipanstack.security.sanitizers import sanitize_sql_identifier

# ReDoS payload against `[^a-zA-Z0-9_]`? No, that's just a simple class negation.
# What about massive string parsing for integer limits? Not applicable here.

import json
from taipanstack.security.models import SecureBaseModel

# Let's check models recursion and massive dicts.

massive_dict = {}
current = massive_dict
for i in range(150):
    current["a"] = {}
    current = current["a"]

class MyModel(SecureBaseModel):
    data: dict

m = MyModel(data=massive_dict)
try:
    print(m.model_dump()["data"])
except Exception as e:
    print("Error:", e)
