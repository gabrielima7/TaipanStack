with open("src/taipanstack/resilience/retry.py") as f:
    print(f.read().find("return last_result, None, True"))
