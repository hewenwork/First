import os
import chardet


class DeDuplication:

    def __init__(self):
        pass

    def get_file_encoding(self, file_path):
        try:
            with open(file_path, "rb")as file:
                encoding = chardet.detect(file.read())["encoding"]
            return encoding
        except chardet.UniversalDetector as e:
            print(e)

