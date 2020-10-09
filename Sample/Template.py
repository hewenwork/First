# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:Template.py
@time:2020/09/02
"""
from datetime import datetime

def log(function):
    def run(*args, **kwargs):
        function_name = function.__name__
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = "function: {}, Exception:{}".format(function_name, e)
        with open("Template-{}.log".format(datetime.today().strftime("%Y%m%d")), "a+")as file:
            line = "{}: {}\n".format(datetime.today(), result)
            file.write(line)
        return result
    return run
 
 
 
 class Main:
    
    def __init__(self, *args, **kwargs):
        print("This is Templates")
 
if __name__ == "__main__":
    Main()
