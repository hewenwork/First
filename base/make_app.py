import os
from base.get_ico import Ico
from subprocess import check_output, SubprocessError


class MakeApplication:

    def __init__(self):
        self.icon_path = Ico().get_ico_path()
        self.script_dir = self.get_script_dir()
        self.dist_dir = os.path.join(os.path.expanduser("~"), r"Desktop")
        self.tempdir = os.path.join(os.path.expanduser("~"), r"AppData\Local\Temp")
        self.start_make()

    @staticmethod
    def get_script_dir():
        command = "where python"
        try:
            python_path = check_output(command)
            python_dir = os.path.dirname(bytes.decode(python_path))
            script_dir = os.path.join(python_dir, "Scripts")
            return script_dir
        except SubprocessError as e:
            exit(e)

    def start_make(self):
        input_file = input(u"需要打包的文件").replace("\"", "")
        os.chdir(self.script_dir)
        command = "python pyinstaller-script.py -F %s -i %s --distpath %s" % (input_file, self.icon_path, self.dist_dir)
        result = os.popen(command).read()
        print(result)


if __name__ == "__main__":
    MakeApplication()
