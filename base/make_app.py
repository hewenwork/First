import os
import requests


class MakeApplication:

    def __init__(self):
        self.python_environment_path = self.get_script_dir()
        self.dist_dir = os.path.join(os.path.expanduser("~"), r"Desktop")
        self.tempdir = os.path.join(os.path.expanduser("~"), r"AppData\Local\Temp")
        self.icon_path = self.get_ico()

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    def get_ico(self):
        ico_file = os.path.join(os.path.expanduser("~"), r"Desktop\ico.ico")
        if os.path.exists(ico_file):
            return ico_file
        else:
            session = self.get_session()
            ico_url = "https://github.com/hewenwork/First/raw/master/icon/hw.ico"
            result = session.get(ico_url).content
            with open(ico_file, "wb")as file:
                file.write(result)
            return ico_file

    @staticmethod
    def get_script_dir():
        command = "where python"
        python_dir = os.path.dirname(os.popen(command).read().split("\n")[0])
        script_dir = os.path.join(python_dir, r"Scripts")
        return script_dir

    def start_make(self):
        input_file = input(u"需要打包的文件").replace("\"", "")
        os.chdir(self.python_environment_path)
        command = "python pyinstaller-script.py -F %s -i %s --distpath %s -w" % (input_file, self.icon_path, self.dist_dir)
        result = os.popen(command).read()
        print(result)


if __name__ == "__main__":
    MakeApplication().start_make()
