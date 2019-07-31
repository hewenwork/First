import os


def c(fu):
    def ss(*args, **kwargs):
        try:
            fu(*args, **kwargs)
        except os.error as e:
            print(e)
        except TypeError as e:
            print(e)
        return fu

    return ss


class A:

    def __init__(self):
        self.aa = "a"
        self.a("aaa")

    @c
    def a(self, cc):
        xx = os.path.exists("a")
        print(cc)
        print(xx)


class B(A):

    def d(self):
        print(self.aa)


A()
