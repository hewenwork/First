import os
import shutil
from subprocess import check_output, SubprocessError


class Compression:

    def __init__(self):
        self.path_rar = r"C:\Program Files\WinRAR"
        self.path_7z = r"C:\Program Files\7-Zip"

    @staticmethod
    def get_failed_folder(file_path):
        try:
            file_dir = os.path.dirname(file_path)
            dist_dir = os.path.join(os.path.dirname(file_dir), r"处理失败")
            if os.path.exists(dist_dir) is False:
                os.makedirs(dist_dir)
            return dist_dir
        except OSError as e:
            print(e)

    def de_7z(self, file_path, password="infected"):
        os.chdir(self.path_7z)
        dir_path = os.path.dirname(file_path)
        command_dict = {
            ".gz": "7z e -tgzip -p%s -y \"%s\" -o\"%s\"" % (password, file_path, dir_path),
            "zip": "7z e -tzip -p%s -y \"%s\" -o\"%s\"" % (password, file_path, dir_path),
            ".7z": "7z e -t7z -p%s -y \"%s\" -o\"%s\"" % (password, file_path, dir_path),
        }
        file_type = file_path[-3:]
        command = command_dict[file_type]
        try:
            check_output(command, shell=True)
            return True
        except SubprocessError as e:
            print(e)
            return False

    def de_rar(self, file_path, password="infected"):
        os.chdir(self.path_rar)
        dir_path = os.path.dirname(file_path)
        command = "rar e -p%s -y \"%s\" \"%s\"" % (password, file_path, dir_path)
        try:
            check_output(command)
            return True
        except SubprocessError as e:
            print(e)
            return False

    def co_rar(self, file_path, password="infected"):
        os.chdir(self.path_rar)
        result_path = file_path + "[infected].rar"
        command = "rar a -ep -p%s \"%s\" \"%s\"" % (password, result_path, file_path)
        try:
            check_output(command, shell=True)
            return result_path
        except SubprocessError as e:
            print(e)
            return False

    def auto_de_file(self, file_path, dist_dir):
        if file_path[-3:] in [".gz", ".7z", "zip"]:
            if self.de_7z(file_path):
                os.remove(file_path)
            else:
                try:
                    shutil.move(file_path, dist_dir)
                except PermissionError:
                    os.remove(file_path)
        elif file_path[-3:] == "rar":
            if self.de_rar(file_path):
                os.remove(file_path)
            else:
                try:
                    shutil.move(file_path, dist_dir)
                except PermissionError:
                    os.remove(file_path)

    def auto_de_folder(self, folder_path):
        dist_dir = os.path.join(os.path.dirname(folder_path), r"处理失败")
        if os.path.exists(dist_dir) is False:
            os.makedirs(dist_dir)
        init_num = 0
        total_num = len(os.listdir(folder_path))
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            self.auto_de_file(file_path, dist_dir)
            deal_process = int(init_num/total_num*100)
            print("\r Deal %s / %s -- %s%%" % (init_num, total_num, deal_process), end="")


if __name__ == "__main__":
    input_folder = input(u"Drag the folder:\n")
    Compression().auto_de_folder(input_folder)
    Compression().co_rar(input_folder)
