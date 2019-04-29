import os


class MakeApplication:

    def __init__(self):
        self.python_environment_path = r"F:\python\Scripts"
        self.dist_dir = r"C:\Users\hewen\Desktop\自用"
        self.tempdir = r"C:\Users\hewen\AppData\Local\Temp"
        self.icon_path = r"\\192.168.1.254\部门共享\TEST\贺文(HW)\ico.ico"

    def start_make(self):
        input_file = input(u"需要打包的文件").replace("\"", "")
        os.chdir(self.python_environment_path)
        command = "python pyinstaller-script.py -F %s -i %s --distpath %s" % (input_file, self.icon_path, self.dist_dir)
        result = os.popen(command).read()
        print(result)


if __name__ == "__main__":
    MakeApplication().start_make()
