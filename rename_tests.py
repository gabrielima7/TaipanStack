import os
import re

def main():
    test_dir = "tests"
    for filename in os.listdir(test_dir):
        if not filename.startswith("test_") or not filename.endswith(".py"):
            continue

        filepath = os.path.join(test_dir, filename)
        with open(filepath, "r") as f:
            content = f.read()

        # Find all def test_xxx(
        def_pattern = re.compile(r"def (test_[a-zA-Z0-9_]+)\(")
        matches = def_pattern.findall(content)

        has_changes = False
        for match in matches:
            if not match.endswith("_expected"):
                new_name = match + "_expected"
                content = re.sub(rf"def {match}\(", f"def {new_name}(", content)
                has_changes = True

        # Handle async def
        async_def_pattern = re.compile(r"async def (test_[a-zA-Z0-9_]+)\(")
        async_matches = async_def_pattern.findall(content)

        for match in async_matches:
            if not match.endswith("_expected"):
                new_name = match + "_expected"
                content = re.sub(rf"async def {match}\(", f"async def {new_name}(", content)
                has_changes = True

        if has_changes:
            with open(filepath, "w") as f:
                f.write(content)

    # Now rename files
    for filename in os.listdir(test_dir):
        if not filename.startswith("test_") or not filename.endswith(".py"):
            continue

        if not filename.endswith("_expected.py"):
            new_filename = filename[:-3] + "_expected.py"
            os.rename(os.path.join(test_dir, filename), os.path.join(test_dir, new_filename))

if __name__ == "__main__":
    main()
