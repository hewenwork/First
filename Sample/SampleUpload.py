# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:SampleUpload.py
@time:2020/08/03
"""
from ftplib import FTP
from os import path, listdir, remove
from datetime import datetime, timedelta

"""
login(user='anonymous',passwd='', acct='') 登录 FTP 服务器，所有参数都是可选的
pwd() 获得当前工作目录
cwd(path) 把当前工作目录设置为 path 所示的路径
dir ([path[,...[,cb]]) 显示 path 目录里的内容，可选的参数 cb 是一个回调函数，会传递给 retrlines()方法
nlst ([path[,...]) 与 dir()类似， 但返回一个文件名列表，而不是显示这些文件名
retrlines(cmd [, cb]) 给定 FTP命令（如“ RETR filename”），用于下载文本文件。可选的回调函数 cb 用于处理文件的每一行
retrbinary(cmd,cb[,bs=8192[, ra]]) 与 retrlines()类似，只是这个指令处理二进制文件。回调函数 cb 用于处理每一块（块大小默认为 8KB）下载的数据
storlines(cmd, f) 给定 FTP 命令（如“ STOR filename”），用来上传文本文件。要给定一个文件对象 f
storbinary(cmd, f,[,bs=8192]) 与 storlines()类似，只是这个指令处理二进制文件。要给定一个文件对象 f，上传块大小 bs 默认为 8KB
rename(old, new) 把远程文件 old 重命名为 new
delete(path) 删除位于 path 的远程文件
mkd(directory) 创建远程目录
rmd(directory) 删除远程目录
quit() 关闭连接并退出
"""


def connect_ftp(host, port, user, password) -> FTP:
    ftp = FTP()
    try:
        ftp.connect(host, port)
        ftp.login(user, password)
    except Exception as e:
        return e
    return ftp


class Run:

    def __init__(self, **kwargs):
        ftp = self.login(**kwargs)
        dist_dir = kwargs.setdefault("dist_dir")
        source_dir = kwargs.setdefault("source_dir")
        file_path = path.join(source_dir, listdir(source_dir)[0])
        upload_name = datetime.today().strftime("Sample-%Y%m%d.rar")
        delete_name = (datetime.today() - timedelta(days=28)).strftime("Sample-%Y%m%d.rar")
        self.total_size = path.getsize(file_path)
        self.remain_size = self.total_size
        self.upload(ftp, file_path, dist_dir, upload_name)
        self.delete_file(ftp, dist_dir, delete_name)
        remove(file_path)
        ftp.quit()

    @staticmethod
    def login(**kwargs):
        host = kwargs.setdefault("host")
        port = kwargs.setdefault("port")
        user = kwargs.setdefault("user")
        password = kwargs.setdefault("password")
        ftp = FTP()
        ftp.connect(host, port)
        ftp.login(user, password)
        return ftp

    def upload(self, ftp, file_path, upload_dir, upload_name):
        ftp.cwd(upload_dir)
        file = open(file_path, "rb")
        block_size = 1024
        command = "STOR {}".format(upload_name)
        ftp.storbinary(command, file, blocksize=block_size, callback=self.upload_process)
        file.close()

    def upload_process(self, block):
        self.remain_size = self.remain_size - len(block)
        size = self.total_size - self.remain_size
        percent = int(size / self.total_size * 100)
        print(f"\r{size}-{self.total_size}-->percent:{percent}%", end="")

    @staticmethod
    def delete_file(ftp: FTP, file_dir, file_name):
        ftp.cwd(file_dir)
        file_name_list = ftp.nlst()
        ftp.delete(file_name) if file_name in file_name_list else None


test_dict = {
    "host": "192.168.1.254",
    "port": 21,
    "user": "download",
    "password": "iobit201806",
    "dist_dir": "/test/hewen/Hewen",
    "source_dir": r"G:\AutoSample\Exchange\Upload",
}

run_dict = {
    "host": "98.129.229.244",
    "port": 21,
    "user": "pftpiobit",
    "password": "ppeOU3Zs",
    "dist_dir": "/web/content",
    "source_dir": r"G:\AutoSample\Exchange\Upload",
}

Run(**run_dict) if datetime.today().weekday() in [0, 3] else None
