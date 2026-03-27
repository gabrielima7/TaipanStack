import re

with open("src/taipanstack/security/models.py", "r") as f:
    content = f.read()

content = content.replace("return _mask_data(data)  # type: ignore[return-value]", "return _mask_data(data)  # type: ignore[return-value,misc]")
content = content.replace("masked_dict = _mask_data(dumped_dict)", "masked_dict = _mask_data(dumped_dict)  # type: ignore[misc]")

content = content.replace("return json.dumps(masked_dict, indent=indent)  # type: ignore[misc]", "return json.dumps(masked_dict, indent=indent)")
content = content.replace("return json.dumps(masked_dict)  # type: ignore[misc]", "return json.dumps(masked_dict)")


with open("src/taipanstack/security/models.py", "w") as f:
    f.write(content)
