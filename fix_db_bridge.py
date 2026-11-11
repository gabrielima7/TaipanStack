with open("src/taipanstack/bridges/db_bridge.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() == "def __init__(":
        new_lines.append(line.replace("def __init__(", "def __init__(  # type: ignore[no-any-unimported]"))
    elif line.strip() == "async def _execute_single_attempt(":
        new_lines.append(line.replace("async def _execute_single_attempt(", "async def _execute_single_attempt(  # type: ignore[no-any-unimported]"))
    elif line.strip() == "async def _process_attempt(":
        new_lines.append(line.replace("async def _process_attempt(", "async def _process_attempt(  # type: ignore[no-any-unimported]"))
    elif line.strip() == "async def _execute_loop(":
        new_lines.append(line.replace("async def _execute_loop(", "async def _execute_loop(  # type: ignore[no-any-unimported]"))
    elif line.strip() == "async def execute(":
        new_lines.append(line.replace("async def execute(", "async def execute(  # type: ignore[no-any-unimported]"))
    else:
        new_lines.append(line)

with open("src/taipanstack/bridges/db_bridge.py", "w") as f:
    f.writelines(new_lines)
