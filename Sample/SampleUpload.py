# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:SampleUpload.py
@time:2020/08/03
"""
from ftplib import FTP
from datetime import datetime
from subprocess import check_output
from os import path, makedirs, listdir, remove, popen


def log(function):
    def write_log(*args, **kwargs):
        function_name = function.__name__
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = "Exception:{}".format(e)
        with open("SampleUpload.log", "a+", encoding="utf-8")as file:
            attr = datetime.today(), function_name, result
            line = "{}: function: {}, result:{}\n".format(*attr)
            file.write(line)
        return result

    return write_log


@log
def login(**kwargs):
    host = kwargs.setdefault("host")
    port = kwargs.setdefault("port", 21)
    user = kwargs.setdefault("user")
    password = kwargs.setdefault("password")
    ftp = FTP()
    ftp.connect(host, port)
    ftp.login(user, password)
    return ftp


@log
def upload_file(ftp: FTP, file_path, dist_dir, file_name=None):
    ftp.cwd(dist_dir)  # "/web/content"
    upload_name = file_name if file_name else path.basename(file_path)
    with open(file_path, "rb")as file:
        block_size = 1024 * 1024
        ftp.storbinary("STOR {}".format(upload_name), file, blocksize=block_size)
    return "{}上传成功".format(file_path)


@log
def cmd_copy(file_path, dist_path):
    makedirs(dist_path) if path.exists(dist_path) is False else None
    command = "copy \"{}\" \"{}\"".format(file_path, dist_path)
    output = popen(command)
    out = output.read()
    return True if "copied" in out else out


@log
def archive(target, archive_path, pwd="infected"):
    if isinstance(target, list):
        makedirs("temp") if path.exists("temp") else None

        target_path = "\" \"".join(target)
    else:
        target_path = "{}\\*".format(target) if path.isdir(target) else target
    mode = "rar a -df -ep -y -p{} ".format(pwd) if archive_path[-3:] == "rar" else "7z a -sdel -y -p{} ".format(pwd)
    attr = "\"{}\" \"{}\"".format(archive_path, target_path)
    command = mode + attr
    output = check_output(command, shell=False)
    out = output.decode()
    return archive_path if "Ok" in out else out


@log
def extract(file_path, dist_path=None, pwd="infected"):
    dist_path = path.dirname(file_path) if dist_path is None else dist_path
    makedirs(dist_path) if path.isdir(dist_path) and path.exists(dist_path) is False else None
    command = "7z e \"{}\" -o\"{}\" -p{} -y -r".format(file_path, dist_path, pwd)
    output = check_output(command, shell=False)
    out = output.decode()
    return True if "Ok" in out else out


@log
def make_rar(source_path, extract_dir, dist_dir, pwd="infected"):
    extract(source_path, extract_dir, pwd=pwd)
    file_path_list = [path.join(extract_dir, file_name) for file_name in listdir(extract_dir)]
    archive_file_path_list = []
    archive_file_size = 1024 * 1024 * 200
    init_size = 0
    for file_path in file_path_list:
        init_size += path.getsize(file_path)
        if init_size <= archive_file_size:
            archive_file_path_list.append(file_path)
        else:
            target = archive_file_path_list
            archive_name = "sample-{}.rar".format(datetime.today().strftime("%Y%m%d-%H%M%S"))
            archive_path = path.join(dist_dir, archive_name)
            archive(target, archive_path=archive_path)
            init_size = 0


def run():
    # 压缩文件目录
    source_dir = r"G:\AutoSample\Exchange\Source"
    # 压缩文件解压的目录
    extract_dir = r"G:\AutoSample\Exchange\Extract"
    # 压缩解压文件存储目录
    dist_dir = r"G:\AutoSample\Exchange\Upload"
    # 压缩文件路径
    source_path = path.join(source_dir, listdir(source_dir)[0])
    # 制作压缩文件
    make_rar(source_path, extract_dir, dist_dir, pwd="infected")
    # 删除源文件
    remove(source_path)
    # 上传文件
    upload_file_path = path.join(dist_dir, listdir(dist_dir)[0])
    # 登录ftp
    ftp = login(**iobit_data)
    upload_file(ftp, file_path=upload_file_path, dist_dir="/test/hewen/Hewen", file_name="test.rar")


iobit_data = {"host": "192.168.1.254", "port": 21, "user": "download", "password": "iobit201806"}
upload_data = {"host": "98.129.229.244", "port": 21, "user": "pftpiobit", "password": "ppeOU3Zs"}

if __name__ == "__main__":
    run()
