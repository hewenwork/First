import os
import shutil
import hashlib


copy_folder = r"\\192.168.1.39\f\Auto"
base_dir = os.getcwd()


class CompressionFunc:

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
        file_md5 = CompressionFunc.get_file_md5(file_path)
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
        file_name = resource_file.split("/")[-1]
        new_file_path = os.path.join(dist_dir, file_name)
        if os.path.exists(new_file_path):
            os.remove(resource_file)
        else:
            shutil.move(resource_file, dist_dir)

    @staticmethod
    def force_del(file_path):
        local_rar_path = r"C:\Program Files\WinRAR"
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

    @staticmethod
    def rename_all(folder_path):
        file_list = CompressionFunc.get_list(folder_path)

        for file_path in file_list:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                rename_result = CompressionFunc.rename_file(file_path)
                if rename_result is False:
                    CompressionFunc.force_del(file_path)

    @staticmethod
    def decompression(file_path):
        local_rar_path = r"C:\Program Files\WinRAR"
        local_7z_path = r"C:\Program Files\7-Zip"
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
        file_list = CompressionFunc.get_list(folder_path)
        for file_path in file_list:
            decompression_result = self.decompression(file_path)
            if decompression_result is False:
                CompressionFunc.move_file(file_path)
        file_list = CompressionFunc.get_list(folder_path)
        for file_path in file_list:
            decompression_result = self.decompression(file_path)
            if decompression_result is False:
                CompressionFunc.move_file(file_path)

    @staticmethod
    def compression(file_path):
        password = "infected"
        result_path = file_path + "[infected].rar"
        local_rar_path = r"C:\Program Files\WinRAR"
        command = "rar a -ep -p%s %s %s" % (password, result_path, file_path)
        os.chdir(local_rar_path)
        try:
            result = os.popen(command).read()
            if "OK" in result.upper():
                return result_path
            else:
                return False
        except:
            return False

    def final_deal(self, folder_path):
        self.decompression_all(folder_path)
        self.rename_all(folder_path)
        result_path = self.compression(folder_path)
        if result_path:
            command = "copy \"%s\" \"%s\"" % (result_path, copy_folder)
            result = os.popen(command).read()
            print(result)


if __name__ == '__main__':
    input_path = input(u"要解压的文件或文件夹").replace("\"", "")
    CompressionFunc().final_deal(input_path)
