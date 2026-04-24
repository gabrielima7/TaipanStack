import os

filepath = "src/taipanstack/security/models.py"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace("    def model_dump(", "    def model_dump(  # noqa: PLR0913")
content = content.replace("    def model_dump_json(", "    def model_dump_json(  # noqa: PLR0913")

with open(filepath, "w") as f:
    f.write(content)
