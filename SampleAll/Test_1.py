def a():
    print(1)
    bb = b()
    return "a", bb


def b():
    print("b")
    return "b"


def c(path=None, **kwargs):
    print(path)


d = {"path": "path", "url": "url"}
c(path="cc")
