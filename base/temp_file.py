class A:

    def __init__(self, a = "aa"):
        b = "bb"
        print(a, b)


class B(A):

    def __init__(self):
        super().__init__(a = "cc")

if __name__ == "__main__":
    B()