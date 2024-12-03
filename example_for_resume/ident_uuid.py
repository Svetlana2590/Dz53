import uuid

# print(uuid.uuid4())

x = 10
print(x)


def ui():
    global x

    x = x + 2
    print(x)
    return None


ui()
print(x)
