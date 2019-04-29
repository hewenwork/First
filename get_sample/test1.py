import datetime
import time

a = datetime.datetime.today()
time.sleep(2)
b = datetime.datetime.today()
result = str(b-a)[:7]
print(datetime.datetime.strptime(result, "%H:%M:%S").time())