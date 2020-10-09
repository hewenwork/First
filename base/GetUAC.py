# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:GetUAC.py
@time:2020/09/11
"""
import ctypes, sys
#
#
# def is_admin():
#     try:
#         # 检测是否有权限, 1: 有权限, 0:无权限
#         status = ctypes.windll.shell32.IsUserAnAdmin()
#         if status == 1:
#             return True
#         else:
#             a = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
#             print(a)
#     except Exception as e:
#         return e
#
# input(is_admin())
if is_admin():
    input("ok")  # Code of your program here
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
from elevate import elevate
import os
status=ctypes.windll.shell32.IsUserAnAdmin()
input(status)
elevate(show_console = True)
# temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
# print(temp)
input(status)
#
# status=ctypes.windll.shell32.IsUserAnAdmin()
# input(print(os.getuid()))
