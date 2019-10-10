import os
import requests
import datetime
base_dir = r"\\192.168.1.254\部门共享\TEST\朱亚玲\IMF\IMF手动分析\自动收集\源文件\MD5N"


class SmMd5:

    def __init__(self):
        self.get_final_file()

    @staticmethod
    def download_date():
        start_date = input(u"请输入要下载的开始日期. 如2019-05-01 回车继续:\n")
        end_date = input(u"请输入要下载的结束日期, 如2019-05-20 回车继续:\n")
        return start_date, end_date

    @staticmethod
    def write_file(file_path, download_url):
        content = requests.get(download_url).content
        with open(file_path, "wb")as file:
            file.write(content)

    def start_download(self):
        start_date, end_date = self.download_date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        interval_day = (end_date - start_date).days
        file_list = []
        for day in range(interval_day+1):
            download_date = str(start_date + datetime.timedelta(days=day))
            download_url = "http://192.168.1.19:8000/?action=downmd5db&dates={}".format(download_date[:10])
            file_path = os.path.join(base_dir, download_date[:10] + ".db")
            print(download_date[:10])
            file_list.append(file_path)
            self.write_file(file_path, download_url)
        return file_list

    def get_final_file(self):
        file_list = self.start_download()
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        final_file = r"\\192.168.1.254\部门共享\TEST\朱亚玲\IMF\IMF手动分析\自动收集\MD5N{}.db".format(today)
        with open(final_file, "wb")as file:
            for file_path in file_list:
                with open(file_path, "rb")as file1:
                    file.write(file1.read())
        final_dict = {}
        with open(final_file, "rb+")as file:
            for i in file.readlines():
                final_dict[i] = 1
            file.seek(0, 0)
            for j in final_dict:
                file.write(j)


if __name__ == "__main__":
    SmMd5()
    input("MD5N下载完成， 请手动关闭此窗口")
