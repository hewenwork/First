import os
import shutil
import hashlib
from subprocess import check_output

import chardet

base_dir = os.getcwd()
copy_folder = r"\\192.168.1.39\f\Auto"


class Base:

    @staticmethod
    def get_list(folder_path):
        file_list = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            file_list.append(file_path)
        return file_list

    @staticmethod
    def get_file_md5(file_path):
        try:
            with open(file_path, 'rb')as md5_file:
                md5_con = hashlib.md5()
                md5_con.update(md5_file.read())
                md5_result = str(md5_con.hexdigest())
                return md5_result
        except:
            return False

    @staticmethod
    def rename_file(file_path):
        file_md5 = Base.get_file_md5(file_path)
        if file_md5:
            file_dir = os.path.dirname(file_path)
            new_file_name = file_md5 + ".vir"
            new_file_path = os.path.join(file_dir, new_file_name)
            if os.path.exists(new_file_path):
                if new_file_path.upper() != file_path.upper():
                    os.remove(file_path)
                    return True
            else:
                try:
                    os.rename(file_path, new_file_path)
                    return True
                except:
                    return False
        else:
            return False

    @staticmethod
    def move_file(resource_file):
        dist_dir = os.path.join(base_dir, "解压失败")
        if os.path.exists(dist_dir) is False:
            os.makedirs(dist_dir)
        file_name = resource_file.split("/")[-1]
        new_file_path = os.path.join(dist_dir, file_name)
        if os.path.exists(new_file_path):
            os.remove(resource_file)
        else:
            shutil.move(resource_file, dist_dir)


class Compression:

    @staticmethod
    def get_encoding(input_str):
        try:
            encoding_result = chardet.detect(input_str)["encoding"]
        except:
            encoding_result = "utf-8"
        return encoding_result

    @staticmethod
    def decompression_7z(file_path, password="infected"):
        dir_path = os.path.dirname(file_path)
        local_7z_path = r"C:\Program Files\7-Zip"
        os.chdir(local_7z_path)
        command_dict = {
            ".gz": "7z e -tgzip -p%s -y \"%s\" -o\"%s\"" % (password, file_path, dir_path),
            "zip": "7z e -tzip -p%s -y \"%s\" -o\"%s\"" % (password, file_path, dir_path),
            ".7z": "7z e -t7z -p%s -y \"%s\" -o\"%s\"" % (password, file_path, dir_path),
        }
        file_type = file_path[-3:]
        command = command_dict[file_type]
        try:
            result = check_output(command, shell=True)
            encoding = Compression.get_encoding(result)
            if "OK" in bytes.decode(result, encoding=encoding).upper():
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def decompression_rar(file_path, password="infected"):
        local_rar_path = r"C:\Program Files\WinRAR"
        os.chdir(local_rar_path)
        dir_path = os.path.dirname(file_path)
        command = "rar e -p%s -y \"%s\" \"%s\"" % (password, file_path, dir_path)
        try:
            result = check_output(command)
            encoding = Compression.get_encoding(result)
            if "OK" in bytes.decode(result, encoding=encoding).upper():
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def compression(file_path, password="infected"):
        local_rar_path = r"C:\Program Files\WinRAR"
        os.chdir(local_rar_path)
        result_path = file_path + "[infected].rar"
        command = "rar a -ep -p%s \"%s\" \"%s\"" % (password, result_path, file_path)
        try:
            result = check_output(command, shell=True)
            encoding = Compression.get_encoding(result)
            if "OK" in bytes.decode(result, encoding=encoding).upper():
                return result_path
            else:
                return False
        except:
            return False


class FinallyDo:

    @staticmethod
    def de(folder_path):
        path_list = Base.get_list(folder_path)
        type_7z = [".gz", "zip", ".7z"]
        type_rar = ["rar"]
        for file_path in path_list:
            if file_path[-3:] in type_7z:
                result = Compression.decompression_7z(file_path)
                if result:
                    os.remove(file_path)
                else:
                    Base.move_file(file_path)
            elif file_path[-3:] in type_rar:
                result = Compression.decompression_rar(file_path)
                if result:
                    os.remove(file_path)
                else:
                    Base.move_file(file_path)
        path_list_new = Base.get_list(folder_path)
        for file_path in path_list_new:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                if file_path[-3:] in type_7z:
                    result = Compression.decompression_7z(file_path)
                    if result:
                        os.remove(file_path)
                    else:
                        Base.move_file(file_path)
                elif file_path[-3:] in type_rar:
                    result = Compression.decompression_rar(file_path)
                    if result:
                        os.remove(file_path)
                    else:
                        Base.move_file(file_path)

    @staticmethod
    def rename(folder_path):
        path_list = Base.get_list(folder_path)
        for file_path in path_list:
            result = Base.rename_file(file_path)
            if result is False:
                os.remove(file_path)

    @staticmethod
    def copy_comp(folder_path):
        result_path = Compression.compression(folder_path)
        os.system("copy \"%s\" \"%s\"" % (result_path, copy_folder))

    @staticmethod
    def s(folder_path):
        FinallyDo.de(folder_path)
        FinallyDo.rename(folder_path)
        FinallyDo.copy_comp(folder_path)


if __name__ == '__main__':
    input_path = input(u"要解压的文件或文件夹").replace("\"", "")
    FinallyDo.s(input_path)

