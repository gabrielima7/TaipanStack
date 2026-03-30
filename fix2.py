with open("tests/test_watchdog_config.py", "r") as f:
    text = f.read()

text = text.replace(
    '        val: int\n\n    with Path',
    '        val: int\n\n    from pathlib import Path\n    with Path'
)

with open("tests/test_watchdog_config.py", "w") as f:
    f.write(text)

with open("tests/test_bridge_web.py", "r") as f:
    text = f.read()
text = text.replace("        send = MockSend()\n", "")
with open("tests/test_bridge_web.py", "w") as f:
    f.write(text)
