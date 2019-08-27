import os
import chardet
import configparser


class Demo:

    def __init__(self):
        self.con = configparser.ConfigParser()
        self.delete_parser(r"C:\Users\hewen\Desktop\autocollect\Update.ini", "English", "md5=0")

    @staticmethod
    def get_encoding(file_path):
        try:
            with open(file_path, "rb")as file:
                encoding = chardet.detect(file.read())["encoding"]
                return encoding
        except Exception as e:
            print(e)

    @staticmethod
    def delete_file(file_path):
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(e)

    def delete_parser(self, file_path, section, detail):
        try:
            self.con.read(file_path, encoding=self.get_encoding(file_path))
            option, value = detail.split("=")
            if self.con.has_option(section=section, option=option):
                self.con.remove_option(section=section, option=option)
                self.con.write(fp=open(file_path, "w"))
        except PermissionError:
            os.system(f"attrib -R {file_path}")
            self.delete_parser(file_path, section, detail)


if __name__ == "__main__":
    Demo()
