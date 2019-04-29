import hashlib
import os
import shutil
copy_folder = r"\\192.168.1.39\f\Auto"
local_rar_path = r"C:\Program Files\WinRAR"
local_7z_path = r"C:\Program Files\7-Zip"


class CompressionFunc:

    @classmethod
    def get_file_md5(cls, file_path):
        try:
            with open(file_path, 'rb')as md5_file:
                md5_con = hashlib.md5()
                md5_con.update(md5_file.read())
                md5_result = str(md5_con.hexdigest())
                return md5_result
        except:
            return False

    def rename_file(self, file_path):
        file_md5 = self.get_file_md5(file_path)
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

    @classmethod
    def force_del(cls, file_path):
        dir_name = os.path.dirname(file_path)
        result_path = os.path.join(dir_name, "delete.rar")
        command = "rar a -df -ep \"%s\" \"%s\"" % (result_path, file_path)
        os.chdir(local_rar_path)
        try:
            result = os.popen(command).read()
            os.remove(result_path)
            if "Done" in result:
                return True
            else:
                return False
        except:
            return False

    def rename_all(self, folder_path):
        dir_path = os.path.dirname(folder_path)
        failed_path = os.path.join(dir_path, "处理失败")
        if os.path.exists(failed_path) is False:
            os.makedirs(failed_path)
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                result = self.rename_file(file_path)
                if result is False:
                    self.force_del(file_path)

    @staticmethod
    def decompression(file_path):
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
            compression_path = command_dict[file_type][0]
            command = command_dict[file_type][-1]
            os.chdir(compression_path)
            try:
                result = os.popen(command).read()
                if "OK" in result.upper():
                    os.remove(file_path)
                    return True
                else:
                    return False
            except:
                return False
        else:
            return True

    def decompression_all(self, folder_path):
        dir_path = os.path.dirname(folder_path)
        failed_path = os.path.join(dir_path, "处理失败")
        if os.path.exists(failed_path) is False:
            os.makedirs(failed_path)
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            result = self.decompression(file_path)
            if result is False:
                shutil.move(file_path, failed_path)
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            result = self.decompression(file_path)
            if result is False:
                shutil.move(file_path, failed_path)

    @staticmethod
    def compression_folder(folder_path):
        password = "infected"
        result_path = folder_path + "[infected].rar"
        command = "rar a -ep -p%s %s %s" % (password, result_path, folder_path)
        os.chdir(local_rar_path)
        try:
            result = os.popen(command).read()
            if "OK" in result.upper():
                return result_path
            else:
                return False
        except:
            return False

    def decompression_delete_rename_compression_move(self, folder_path):
        self.decompression_all(folder_path)
        self.rename_all(folder_path)
        result_path = self.compression_folder(folder_path)
        if result_path is not False:
            command = "copy \"%s\" \"%s\"" % (result_path, copy_folder)
            result = os.popen(command).read()
            print(result)


if __name__ == '__main__':
    input_path = input(u"要解压的文件或文件夹").replace("\"", "")
    CompressionFunc().decompression_delete_rename_compression_move(input_path)
