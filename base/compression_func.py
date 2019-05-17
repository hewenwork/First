import os
import chardet
from subprocess import check_output


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
        command = command_dict[file_type][-1]
        result = check_output(command)
        encoding = Compression.get_encoding(result)
        if "OK" in bytes.decode(result, encoding=encoding).upper():
            return True
        else:
            return False

    @staticmethod
    def decompression_rar(file_path, password="infected"):
        local_rar_path = r"C:\Program Files\WinRAR"
        os.chdir(local_rar_path)
        dir_path = os.path.dirname(file_path)
        command = "rar e -p%s -y \"%s\" \"%s\"" % (password, file_path, dir_path)
        result = check_output(command)
        encoding = Compression.get_encoding(result)
        if "OK" in bytes.decode(result, encoding=encoding).upper():
            return True
        else:
            return False

    @staticmethod
    def compression(file_path, password="infected"):
        local_rar_path = r"C:\Program Files\WinRAR"
        os.chdir(local_rar_path)
        result_path = file_path + "[infected].rar"
        command = "rar a -ep -p%s \"%s\" \"%s\"" % (password, result_path, file_path)
        result = check_output(command)
        encoding = Compression.get_encoding(result)
        if "OK" in bytes.decode(result, encoding=encoding).upper():
            return result_path
        else:
            return False


