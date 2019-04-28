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
        if os.path.exists(icon_path):
            pass
        else:
            user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
            headers = {"User-Agent": user_agent}
            session = requests.session()
            session.headers.update(headers)
            ico_url = "https://raw.githubusercontent.com/hewenwork/First/master/icon/hw.ico"
            ico = session.get(url=ico_url).content
            with open(icon_path, "wb")as file:
                file.write(ico)

    @classmethod
    def start_make(cls):
        input_file = input(u"python file").replace("\"", "")
        os.chdir(environment_path)
        command = "python pyinstaller-script.py -F %s -i %s --distpath %s" % (input_file, icon_path, user_desktop_path)
        result = os.popen(command).read()
        print(result)


if __name__ == "__main__":
    MakeApplication().start_make()
