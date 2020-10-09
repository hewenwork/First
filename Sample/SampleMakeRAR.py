from subprocess import check_output
from os import path, makedirs, listdir, remove, popen


def execute_cmd(command: str = None):
    output = check_output(command, shell=False)
    out = output.decode()
    return out


test_dict = {
    "host": "192.168.1.254",
    "port": 21,
    "user": "download",
    "password": "iobit201806",
    "dist_dir": "/test/hewen/Hewen",
    "source_dir": r"G:\AutoSample\Exchange\Upload",
    "archive_dir": r"C:\Users\hewen\Desktop\Kafan",
    "extract_dir": r"G:\AutoSample\Exchange\Extract"
}

run_dict = {
    "host": "98.129.229.244",
    "port": 21,
    "user": "pftpiobit",
    "password": "ppeOU3Zs",
    "dist_dir": "/web/content",
    "source_dir": r"G:\AutoSample\Exchange\Upload",
    "archive_dir": r"G:\AutoSample\Exchange\Source",
    "extract_dir": r"G:\AutoSample\Exchange\Extract"
}


def archive(file_path: str, archive_path: str = None, password: str = "infected"):
    if file_path is None:
        return "file_path is None"
    if archive_path is None:
        file_dir = path.dirname(file_path)
        archive_name = "[{}]{}.zip".format(password, path.basename(file_path).split(".")[0])
        archive_path = path.join(file_dir, archive_name)
    if ".rar" in archive_path:
        attr_mode = "rar a -ep -p{} -y".format(password)
        attr_archive = "\"{}\"".format(archive_path)
        attr_file = "\"{}\"".format(file_path)
    else:
        attr_mode = "7z a -ep -p{} -y".format(password)
        attr_archive = "\"{}\"".format(archive_path)
        attr_file = "\"{}\\*\"".format(file_path) if path.isdir(file_path) else "\"{}\"".format(file_path)
    command = attr_mode + attr_archive + attr_file
    execute_result = execute_cmd(command)
    return True if "Ok" in execute_result else execute_result


def extract(archive_path, dist_dir, password="infected"):
    command = "7z e \"{}\" -o\"{}\" -p{} -y -r".format(archive_path, dist_dir, password)
    output = check_output(command, shell=False)
    out = output.decode()
    return True if "Ok" in out else out


def make_archive(file_dir):
    archive_size = 1024 * 1024 * 200
    total_size = 0
    file_path_list = []
    for file_name in listdir(file_dir):
        file_path = path.join(file_dir, file_name)
        file_size = path.getsize(file_path)
        total_size += file_size
        if total_size >= archive_size:
            break
        else:
            file_path_list.append(file_path)
    return file_path_list



class MakeRar:
    archive_dir = ""
    extract_dir = ""

    def __init__(self, **kwargs):
        archive_file_path = self.get_file_path(kwargs)
        extract_dir = kwargs.setdefault("extract_dir")
        archive_dir = kwargs.setdefault("archive_dir")
        if len(listdir(archive_dir)) >= 20:
            pass
        else:
            self.run(archive_file_path, extract_dir)

    def flow(self):
        """
        1. 判断剩余可用的压缩包是否多余50
        1.1 多余50 --pass
        1.2 低于50
            1.2.1 解压压缩包到指定目录
            1.2.2 指定目录文件按照200M分类
            1.2.3 压缩分类的文件
            1.2.4 转移到压缩包目录
        """

    @staticmethod
    def get_file_path(kwargs: dict) -> str:
        archive_dir = kwargs.setdefault("archive_dir")
        file_name_list = [file_name for file_name in listdir(archive_dir) if ".zip" in file_name]
        file_path_list = [path.join(archive_dir, file_name) for file_name in file_name_list]
        file_path = file_path_list[0]
        return file_path

    def run(self, archive_file_path, extract_dir):
        extract(archive_file_path, extract_dir)
        file_path_list = [path.join(extract_dir, file_name) for file_name in listdir(extract_dir)]
        init_size = 0
