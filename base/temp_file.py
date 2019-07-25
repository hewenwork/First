import time
from multiprocessing import Pool, freeze_support
freeze_support()


class Aaa:

    def __init__(self):
        print("__init__")

    @classmethod
    def ab(cls):
        print("classmethod")


# def aa(i):
#     print(f"I am {i}: Running")
#     time.sleep(15)
#     print(f"I am {i}:", time.time())
#
#
if __name__ == "__main__":
    Aaa.ab()
#     po = Pool(2)
#     a = 1
#     while True:
#         if time.strftime("%S")[-1] == "2":
#             time.sleep(1)
#             po.apply_async(func=aa, args=(a, ))
#             a += 1
