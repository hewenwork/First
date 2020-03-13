# encoding = utf-8
# @Author: Hewen
# @Time: 11/8/2019 12:41 PM
# @File: FTPFunc.py
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

import os
import socket
import ftplib


class FTPFunc:

    def __init__(self, host, port, user, pwd):
        self.ftp = self.login(host, port, user, pwd) if True else exit('?')
        # self.upload(r"C:\Users\hewen\Desktop\add.txt", r"/web/content")

    @staticmethod
    def login(host, port, user, pwd):
        ftp = ftplib.FTP()
        try:
            ftp.connect(host, port)
            ftp.login(user, pwd)
            return ftp
        except socket.gaierror and ftplib.error_perm:
            return u"链接错误, 账户密码不正确"

    def upload(self, path_target, path_dist, dist_name=None):
        if dist_name is None:
            dist_name = os.path.basename(path_target)
        try:
            self.ftp.cwd(path_dist)
            file = open(path_target, "rb")
            self.ftp.storbinary(f"STOR {dist_name}", file)
            file.close()
        except ftplib.error_temp as e:
            exit(f"远程目录错误: {e}")
        except OSError as e:
            exit(f"文件不存在, 不正确 {e}")
        else:
            self.ftp.quit()
            return True

    def download(self, path_file, path_dist):
        pass


if __name__ == "__main__":
    host1, port1 = "98.129.229.244", 21
    user1, pwd1 = "pftpiobit", "IObit20110617"
    FTPFunc(host1, port1, user1, pwd1)
