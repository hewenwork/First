# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:FunctionConfig.py
@time:2020/07/24
"""
from datetime import datetime


def log(function):
    def run(*args, **kwargs):
        function_name = function.__name__
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = "function: {}, Exception:{}".format(function_name, e)
        print(result) if result is not True else None
        return result

    return run


class Main:

    def __init__(*args, **kwargs):
        print("This is Templates")


if __name__ == "__main__":
    Main()
