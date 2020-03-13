# encoding = utf-8
# @Author: Hewen
# @Time: 10/28/2019 2:29 PM
# @File: AutoUpdate.py
import hashlib
import os
import socket


class AutoUpdate:

    def __init__(self):

        self.start_sever()

    @staticmethod
    def start_sever():
        host_name = socket.gethostname()
        host = socket.gethostbyname(host_name)
        test_info = f'''[Main]\nUpdateUrl=http://{host}/Update.ini'''
        file_path = r"TestUpdate.ini"
        with open(file_path, "w")as file:
            file.write(test_info)
        file_dir = os.path.dirname(__file__)
        os.chdir(file_dir)
        command = f"python -m http.server 80"
        os.system(command)

    @staticmethod
    def file_md5(file_path):
        md5_object = hashlib.md5()
        try:
            with open(file_path, "rb")as file:
                md5_object.update(file.read())
            md5_result = md5_object.hexdigest()
        except OSError:
            return False
        else:
            return md5_result

    @staticmethod
    def get_detail(file_path):
        file_size = os.path.getsize(file_path)
        file_md5 = AutoUpdate.file_md5(file_path)



if __name__ == "__main__":
    AutoUpdate()
