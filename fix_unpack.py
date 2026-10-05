with open("src/taipanstack/resilience/retry.py", "r") as f:
    content = f.read()

# Ah! In my regex replacement I added ", True" to "return last_result, None", but there was another one inside `_run_sync_attempt` which already had ", True" and so it became ", True, True". Wait, no, `_run_sync_attempt` returns a 3-tuple `(last_result, None, True)`. If I replaced it everywhere, it would have replaced the one inside the loop logic.

# Let's write a python script to fix the return values of `_run_async_retry_loop` and `_run_sync_retry_loop`.

import re
import sys

def fix():
    with open("src/taipanstack/resilience/retry.py", "r") as f:
        content = f.read()

    content = content.replace("return last_result, None, True, True", "return last_result, None, True")

    with open("src/taipanstack/resilience/retry.py", "w") as f:
        f.write(content)

fix()
