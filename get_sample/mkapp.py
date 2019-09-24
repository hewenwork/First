# coding:utf-8
import os
import PyInstaller.__main__


class MakeApp:
    icon = r"F:\Workspace\First\icon\ico.ico"
    temp = os.path.join(os.path.expanduser("~"), r"AppData\Local\Temp")
    distpath = os.path.join(os.path.expanduser("~"), "Desktop")

    def __init__(self, file_path):
        os.chdir(self.temp)
        try:
            PyInstaller.__main__.run(
                [
                    f"--icon={self.icon}",
                    f"--onefile",
                    "--noconfirm",
                    "--distpath",
                    self.distpath,
                    "--specpath",
                    self.temp,
                    "--clean",
                    # "--noconsole",
                    file_path
                ]
            )
        except Exception as e:
            print(e)


if __name__ == "__main__":
    file_make = r"F:\Workspace\First\tool\AutoDownUpload.py"
    MakeApp(file_make)
