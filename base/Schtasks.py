# encoding = utf-8
# @Author: Hewen
# @Time:  17:51
import re
import subprocess
from subprocess import getstatusoutput, SubprocessError, Popen
# import commands

class Schtasks:

    def __init__(self):
        # self.create("this", r"C:\Users\hewen\Desktop\add.txt", "once")
        print(self.tasks())

    def create(self, name_script, path_script, schedule, time_start="15:00:00"):
        if name_script in self.tasks():
            return True
        else:
            command = f"schtasks /create /sc {schedule} /st {time_start} /tn {name_script} /tr \"{path_script}\""
        if schedule in ["MINUTE", "HOURLY", "DAILY", "WEEKLY、MONTHLY、ONCE、ONSTART、ONLOGON、ONIDLE"]:
            pass
        command = f"schtasks /create /sc {schedule} /st {time_start} /tn {name_script} /tr \"{path_script}\""

    def run(self):
        command = ""

    def delete(self):
        commad = ""

    @staticmethod
    def tasks():
        command = r"schtasks /query /fo list"
        try:
            result = getstatusoutput(command)
        except SubprocessError as e:
            exit(e)
        else:
            if result[0] == 0:
                result = result[-1]
                tasks_dict = dict(zip(re.findall(r"TaskName:\s*\\(.*)", result), re.findall(r"Status:\s*(.*)", result)))
                return tasks_dict
            else:
                exit("Error")


if __name__ == "__main__":
    # Schtasks()
    # def aa(aaa, info):
    #     with open(r"C:\Users\hewen\Desktop\%s.txt" % aaa, "w")as file:
    #         file.write(info)
    # a = Popen("schtasks /query /fo list", shell=True, stdout=aa("out", subprocess.PIPE), stderr=aa("in", subprocess.PIPE))
    a = Popen("schtasks /query /fo list", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(a.stdout.read())
