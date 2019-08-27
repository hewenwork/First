import os
import chardet


class DeDuplication:

    def __init__(self):
        pass

    @staticmethod
    def get_encoding(file_path):
        try:
            with open(file_path, "rb")as file:
                encoding = chardet.detect(file.read())["encoding"]
            return encoding
        except Exception as e:
            print(e)
            return

    @staticmethod
    def get_all_file(folder):
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            if os.path.isdir(file_path):
                DeDuplication().get_all_file(file_path)
            else:
                if os.path.split(file_path)[-1] == "SignatureN.db":
                    print(file_path)
                    with open(r"C:\Users\hewen\Desktop\La.txt", "a+", encoding="utf-8")as file:
                        file.write(open(file_path, "r+", encoding="utf-8").read())

    @staticmethod
    def find_sign():
        for file_name in os.listdir(r"F:\数据库\Database"):
            print()


if __name__ == "__main__":
    # DeDuplication().get_all_file(r"F:\数据库\Database")
    dict_test = []
    with open(r"C:\Users\hewen\Desktop\La.txt", "r+", encoding="utf-8")as file:
        for line in file.readlines():
            line = line[13:]
            if line not in dict_test:
                dict_test.append(line)
            else:
                with open(r"C:\Users\hewen\Desktop\Laaa.txt", "a+", encoding="utf-8")as file1:
                    file1.write(line)
