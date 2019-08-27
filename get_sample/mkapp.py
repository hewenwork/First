# coding:utf-8
import os
import PyInstaller.__main__


class MakeApp:

    def __init__(self, file_path):
        self.a = r"C:\Users\hewen\Desktop"
        self.icon = r"C:\Users\hewen\Desktop\ico.ico"
        self.temp = os.path.join(os.path.expanduser("~"), r"AppData\Local\Temp")
        self.distpath = os.path.join(os.path.expanduser("~"), "Desktop")
        self.workpath = r"F:\ss"
        self.specpath = r"F:\ss"
        self.make(file_path)

    def make(self, file_path):
        os.chdir(r"F:\python\Scripts")
        command = f"pyinstaller.exe -F {file_path} -i {self.icon} –-distpath {self.distpath} –-workpath {self.workpath} –-specpath {self.temp} –-clean -y"
        try:
            PyInstaller.__main__.run(
                [
                    # f"--name=dd"
                    f"--icon={self.icon}",
                    f"--onefile",
                    "--noconfirm",
                    # "--clear",
                    __file__
                ]
            )
        except Exception as e:
            print(e)


if __name__ == "__main__":
    file_make = r"F:\Workspace\First\get_sample\mkapp.py"
    MakeApp(file_make)
