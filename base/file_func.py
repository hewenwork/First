import subprocess

a = subprocess.call("ipconfig", shell=True)
print(a)