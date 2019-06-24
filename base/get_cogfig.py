import configparser
from base.base_func import Base


class ConfigFunc:

    def __init__(self, file_path):
        self.config = configparser.ConfigParser()
        encoding = Base().get_encoding(file_path)
        self.config.read(file_path, encoding=encoding)
        self.config.sections()

cofig = ConfigFunc(r"C:\Users\hewen\Desktop\Update.ini").config["PatchUpdate"]
print(cofig.get("FileServer"))
