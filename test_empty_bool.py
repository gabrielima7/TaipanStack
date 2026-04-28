def my_gen():
    yield "ls"

print(bool(my_gen()))
