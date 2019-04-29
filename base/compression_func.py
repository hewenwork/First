import hashlib
import os
import shutil

local_rar_path = r"C:\Program Files\WinRAR"
local_7z_path = r"C:\Program Files\7-Zip"
compression_failed_folder = r"F:\auto_collect\解压失败"
rename_failed_folder = r"F:\auto_collect\重命名失败"

copy_folder = r"\\192.168.1.39\f\Auto"


class Compression:

    # def __init__(self):
    # self.local_rar_path = r"C:\Program Files\WinRAR"
    # self.local_7z_path = r"C:\Program Files\7-Zip"
    # self.compression_failed_folder = r"F:\auto_collect\解压失败"
    # self.rename_failed_folder = r"F:\auto_collect\重命名失败"
    # self.smartccl_folder = r"\\192.168.1.39\f\Auto"

    @staticmethod
    def get_file_md5(file_path):
        try:
            with open(file_path, 'rb')as md5_file:
                md5_con = hashlib.md5()
                md5_con.update(md5_file.read())
                md5_result = str(md5_con.hexdigest()).upper()
                return md5_result
        except:
            return False

    def rename_file(self, file_path):
        file_md5 = self.get_file_md5(file_path)
        if file_md5:
            file_dir = os.path.dirname(file_path)
            new_file_name = file_md5 + ".vir"
            new_file_path = os.path.join(file_dir, new_file_name)
            if file_path != new_file_path and os.path.exists(new_file_path) is False:
                os.rename(file_path, new_file_path)
                return True
            elif file_path != new_file_path and os.path.exists(new_file_path):
                os.remove(file_path)
                return True
            elif file_path == new_file_path:
                return True
        else:
            shutil.move(file_path, rename_failed_folder)

    def rename_all(self, folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            file_size = os.path.getsize(file_path)
            if file_size < 1024:
                try:
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    elif os.path.isfile(file_path):
                        os.remove(file_path)
                except:
                    shutil.move(file_path, rename_failed_folder)
            else:
                result = self.rename_file(file_path)
                if result is False:
                    shutil.move(file_path, rename_failed_folder)

    @classmethod
    def decompression(self, file_path):
        password = "infected"
        dir_path = os.path.dirname(file_path)
        command_dict = {
            ".gz": [local_7z_path, "7z e -tgzip -p%s -y \"%s\" -o%s" % (password, file_path, dir_path)],
            "zip": [local_7z_path, "7z e -tzip -p%s -y \"%s\" -o%s" % (password, file_path, dir_path)],
            ".7z": [local_7z_path, "7z e -t7z -p%s -y \"%s\" -o%s" % (password, file_path, dir_path)],
            "rar": [local_rar_path, "rar e -p%s -y \"%s\" %s" % (password, file_path, dir_path)]
        }
        file_type = file_path[-3:]
        if file_type in command_dict.keys():
            try:
                compression_path = command_dict[file_type][0]
                command = command_dict[file_type][-1]
                os.chdir(compression_path)
                result = os.popen(command).read()
                if "OK" in result.upper():
                    return True
                else:
                    return False
            except:
                return False
        else:
            return None

    def decompression_all(self, folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            result = self.decompression(file_path)
            if result is True:
                os.remove(file_path)
            elif result is False:
                shutil.move(file_path, compression_failed_folder)
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            result = self.decompression(file_path)
            if result is True:
                os.remove(file_path)
            elif result is False:
                shutil.move(file_path, compression_failed_folder)

    @classmethod
    def compression_folder(cls, folder_path):
        try:
            password = "infected"
            result_path = folder_path + "[infected].rar"
            command = "rar a -ep -p%s %s %s" % (password, result_path, folder_path)
            os.chdir(local_rar_path)
            result = os.popen(command).read()
            if "OK" in result.upper():
                return result_path
            else:
                return False
        except:
            return False

    def compression_delete_rename_compression_move(self, folder_path):
        self.decompression_all(folder_path)
        self.rename_all(folder_path)
        result_path = self.compression_folder(folder_path)
        os.popen("copy %s[infected].rar %s" % (result_path, copy_folder))


if __name__ == '__main__':
    input_path = input("folder").replace("\"", "")
    Compression().compression_delete_rename_compression_move(input_path)