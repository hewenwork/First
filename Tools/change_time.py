# 修改系统时间
import os
from subprocess import check_output

a = check_output("chcp 437", shell=True)
b = check_output("date", shell=True)
print(bytes.decode(b))