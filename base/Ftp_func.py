import os
import datetime
from ftplib import FTP
'''
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
'''


class FtpFunc:

    def __init__(self):
        self.date = datetime.datetime.today().strftime("%Y%m%d")
        self.ftp = self.get_login()
        self.upload_file = self.get_file()
        self.upload_file_name = "samples-%s.rar" % self.date
        self.ftp.cwd("/web/content/")
        with open(self.upload_file, "rb")as file:
            self.ftp.storbinary("STOR %s" % self.upload_file_name, file)

    @staticmethod
    def get_login():
        ftp = FTP()
        host, port = "98.129.229.244", 21
        user, pwd = "pftpiobit", "IObit20110617"
        ftp.connect(host, port)
        ftp.login(user, pwd)
        if "server ready" in ftp.getwelcome():
            return ftp
        else:
            exit("Ftp Error")

    def get_file(self):
        local_folder = r"E:\交换样本\上传"
        upload_file_name = "samples-%s.rar" % self.date
        upload_file = os.path.join(local_folder, upload_file_name)
        if os.path.exists(upload_file):
            return upload_file
        else:
            exit("No File")


if __name__ == "__main__":
    FtpFunc()
