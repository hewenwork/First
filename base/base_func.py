import os
import shutil
import chardet
import hashlib
import datetime
from subprocess import check_output, SubprocessError


class Base:

    @staticmethod
    def get_date(days=1):
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=days)
        date = today - time_interval
        return date

    @staticmethod
    def switch_vpn(turn):
        print("Switch VPN " + turn)
        connect_command = "rasdial  US usa vpn2014"
        disconnect_command = "rasdial US /DISCONNECT"
        command_dict = {
            "on": connect_command,
            "off": disconnect_command
        }
        try:
            check_output(command_dict[turn], shell=True)
        except SubprocessError as e:
            print(e)

    @staticmethod
    def get_encoding(file_path):
        if os.path.isfile(file_path):
            with open(file_path, "rb")as file:
                encoding = chardet.detect(file.read())["encoding"]
        else:
            encoding = chardet.detect(file_path)["encoding"]
        return encoding

    @staticmethod
    def get_file_md5(file_path):
        try:
            with open(file_path, "rb")as md5_file:
                md5_con = hashlib.md5()
                md5_con.update(md5_file.read())
                md5_result = str(md5_con.hexdigest())
                return md5_result.upper()
        except OSError as e:
            print(file_path, e, sep="\n")

    @staticmethod
    def get_list(folder_path):
        try:
            file_list = []
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                file_list.append(file_path)
            return file_list
        except FileNotFoundError as e:
            print(e)

    @staticmethod
    def copy_file(file_path, dist_dir):
        command = "copy \"%s\" \"%s\"" % (file_path, dist_dir)
        try:
            os.system(command, shell=True)
        except OSError as e:
            print(e)

    @staticmethod
    def rename_file(file_path):
        if os.path.isfile(file_path):
            file_md5 = Base.get_file_md5(file_path)
            file_path_new = os.path.join(os.path.dirname(file_path), file_md5 + ".vir")
            try:
                shutil.move(file_path, file_path_new)
            except shutil.Error as e:
                print(file_path, e, sep="\n")
        else:
            shutil.rmtree(file_path)

    @staticmethod
    def move_file(file_path, dist_dir):
        try:
            file_name = os.path.basename(file_path)
            file_path_new = os.path.join(dist_dir, file_name)
            shutil.move(file_path, file_path_new)
        except FileNotFoundError as e:
            print(e)
        except shutil.Error as e:
            print(e)



