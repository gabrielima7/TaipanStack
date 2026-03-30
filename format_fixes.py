with open("tests/test_bridge_web.py", "r") as f:
    text = f.read()
text = text.replace(
    '        send = MockSend()\n        from taipanstack.bridges.web_bridge import result_to_response; result_to_response(Err(ValueError("err")))',
    '        from taipanstack.bridges.web_bridge import result_to_response\n        result_to_response(Err(ValueError("err")))'
)
with open("tests/test_bridge_web.py", "w") as f:
    f.write(text)

with open("tests/test_watchdog_config.py", "r") as f:
    text = f.read()
text = text.replace(
    '    with open("test_bad_validate.json", "w") as f:',
    '    with Path("test_bad_validate.json").open("w") as f:'
)
text = text.replace(
    '    os.remove("test_bad_validate.json")',
    '    Path("test_bad_validate.json").unlink()'
)
text = text.replace(
    '    with open("test_good_validate.json", "w") as f:',
    '    with Path("test_good_validate.json").open("w") as f:'
)
text = text.replace(
    '    os.remove("test_good_validate.json")',
    '    Path("test_good_validate.json").unlink()'
)
with open("tests/test_watchdog_config.py", "w") as f:
    f.write(text)

with open("tests/test_watchdog_health.py", "r") as f:
    text = f.read()
text = text.replace(
    '    from taipanstack.core.result import Ok; assert res == Ok({"t1": False})',
    '    from taipanstack.core.result import Ok\n    assert res == Ok({"t1": False})'
)
with open("tests/test_watchdog_health.py", "w") as f:
    f.write(text)
