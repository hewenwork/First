import os
import shutil
import chardet
import hashlib
import requests
import datetime
import subprocess


base_dir = os.getcwd()


class Base:

    @staticmethod
    def get_encoding(file_path):
        if os.path.isfile(file_path):
            with open(file_path, "rb")as file:
                encoding = chardet.detect(file.read())["encoding"]
        else:
            encoding = chardet.detect(file_path)["encoding"]
        return encoding

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
    def get_sample_folder():
        download_data = Base.get_date()
        sample_folder = os.path.join(base_dir, download_data)
        if os.path.exists(sample_folder) is False:
            os.makedirs(sample_folder)
        return sample_folder

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    @staticmethod
    def get_file_md5(file_path):
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb")as md5_file:
                    md5_con = hashlib.md5()
                    md5_con.update(md5_file.read())
                    md5_result = str(md5_con.hexdigest())
                    return md5_result.upper()
            except:
                return False
        else:
            return False

    @staticmethod
    def get_list(folder_path):
        file_list = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            file_list.append(file_path)
        return file_list

    @staticmethod
    def get_date(days=1):
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=days)
        download_day = today - time_interval
        return download_day.strftime("%Y-%m-%d")

    @staticmethod
    def write_sample(sample_path, sample_download_url, session=None):
        if session is None:
            session = Base.get_session()
        if os.path.exists(sample_path):
            return True
        else:
            try:
                response = session.get(url=sample_download_url, stream=True)
                if response.status_code == 200:
                    with open(sample_path, "wb")as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            file.write(chunk)
                    return True
                else:
                    return False
            except:
                return False

    @staticmethod
    def switch_vpn():
        os.system("chcp 437")
        connect_status = "netstat -an"
        connect_command = "rasdial  US usa vpn2014"
        disconnect_command = "rasdial US /DISCONNECT"
        result = os.popen(connect_status).read()
        if "1723" in result:
            os.popen(disconnect_command).read()
        else:
            os.popen(connect_command).read()

    @staticmethod
    def copy_file(resource_path, dist_path):
        command = "copy \"%s\" \"%s\"" % (resource_path, dist_path)
        os.system(command)

    @staticmethod
    def write_md5(md5):
        download_date = Base.get_date()
        md5_file_path = os.path.join(base_dir, r"md5_info/%s.txt" % download_date)
        if os.path.exists(md5_file_path):
            with open(md5_file_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(md5 + "\n" + old_data)
        else:
            with open(md5_file_path, "a+")as file:
                file.seek(0, 0)
                file.write(md5 + "\n")

    @staticmethod
    def write_log(result):
        log_path = os.path.join(base_dir, "download_log.txt")
        write_date = datetime.datetime.now().strftime("%Y%m%d %H%M%S")
        data = "%s %s" % (write_date, result)
        if os.path.exists(log_path):
            with open(log_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(data + "\n" + old_data)
        else:
            with open(log_path, "a+")as file:
                file.write(data + "\n")

    @staticmethod
    def rename(file_path):
        file_md5 = Base.get_file_md5(file_path)
        new_file_path = os.path.join(os.path.dirname(file_path), file_md5 + ".vir")
        if new_file_path == file_path:
            if os.path.exists(new_file_path):
                return True
        else:
            os.renames(file_path, new_file_path)

