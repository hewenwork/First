import os
from subprocess import check_output


class CreatFile:

    @staticmethod
    def get_user_path():
        desktop_path = os.path.join(os.path.expanduser("~"), r"Desktop\testfile.file")
        return desktop_path

    @staticmethod
    def make_file():
        desktop_path = os.path.join(os.path.expanduser("~"), r"Desktop\testfile.file")
        if os.path.exists(desktop_path):
            os.remove(desktop_path)
        else:
            command = ""
            result = check_output(command)
