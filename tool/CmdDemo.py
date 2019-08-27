import os
import sys
import ctypes


class GetAdmin:

    def __init__(self, func):
        task_name = "HewenSkip"
        real_path = os.path.realpath(sys.argv[0])
        if ctypes.windll.shell32.IsUserAnAdmin() == 1:
            if task_name in os.popen("schtasks /query /fo LIST /v").read():
                func()
            else:
                command = f"schtasks /create /tn {task_name} /tr {real_path} /sc ONLOGON /rl HIGHEST "
                os.system(command)
                func()
        else:
            if task_name in os.popen("schtasks /query /fo LIST /v").read():
                os.system(f"schtasks /run /tn {task_name}")
            else:
                ctypes.windll.shell32.ShellExecuteW(None, u"runas", sys.executable, real_path, None, 1)


if __name__ == "__main__":
    GetAdmin(1)
