import os
import requests

python_dir = os.path.dirname(os.popen("where python").read())
environment_path = os.path.join(python_dir, "Scripts")
user_path = os.path.expanduser("~")
user_desktop_path = os.path.join(user_path, "Desktop")
temp_dir = os.path.join(user_path, r"AppData\Local\Temp")
icon_path = os.path.join(temp_dir, "ico.ico")


class MakeApplication:

    def __init__(self):

        self.dist_dir = r"C:\Users\hewen\Desktop\自用"
        self.tempdir = r"C:\Users\hewen\AppData\Local\Temp"
        self.get_ico()

    @classmethod
    def get_ico(cls):
        ico_url = "https://raw.githubusercontent.com/hewenwork/First/master/icon/hw.ico"
        ico = requests.get(url=ico_url).content
        with open(icon_path, "wb")as file:
            file.write(ico)

    @classmethod
    def start_make(cls):
        input_file = input(u"需要打包的文件").replace("\"", "")
        os.chdir(environment_path)
        command = "python pyinstaller-script.py -F %s -i %s --distpath %s -w " % (input_file, icon_path, user_desktop_path)
        result = os.popen(command).read()
        print(result)


if __name__ == "__main__":
    MakeApplication().start_make()
