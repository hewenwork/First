import os
import base64
import requests


class GetBugreport:

    def __init__(self):
        self.download_date = self.get_date()
        self.product = self.get_product()
        self.base_dir = self.get_base_dir()

    @staticmethod
    def get_base_dir():
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        base_dir = os.path.join(desktop_path, "BugReport")
        if os.path.exists(base_dir)is False:
            os.mkdir(base_dir)
        return base_dir

    @staticmethod
    def get_product():
        product_name = input(u"请输入产品名对应的数字\n1:IU\n2:IMF \n3:ISU\n")
        product_dict = {
            "1": "iu",
            "2": "imf",
            "3": "su",
            "4": "asc",
            "5": "ascu",
            "6": "db",
            "7": "sd"
        }
        product = product_dict[product_name]
        return product

    @staticmethod
    def get_date():
        download_date = input(u"请输入下载日期如2019-05-14\n")
        return download_date

    def get_report(self):
        download_dir = os.path.join(self.base_dir, r"%s\%s" % (self.product, self.download_date))
        if os.path.exists(download_dir) is False:
            os.makedirs(download_dir)
        url = "http://ascstats.iobit.com/other/bugReport/json_today/json_today.php"
        params = {
            "table": "%s_bugreport_v2" % self.product,
            "date": self.download_date
        }
        try:
            response = requests.get(url=url, params=params)
            return_size = int(response.headers["content-length"])
            if return_size <= 1024:
                print("No Data")
            else:
                for user_num in response.json():
                    file_name = user_num["id"] + user_num["email"] + ".zip"
                    file_path = os.path.join(download_dir, file_name)
                    with open(file_path, "wb")as file:
                        bugcontent = base64.b64decode(user_num["bugcontent"])
                        file.write(bugcontent)
                    print("#"*len(response.json()))
        except requests.RequestException as e:
            print(e)


if __name__ == "__main__":
    print(u"Bugreport获取程序\nstart====")
    GetBugreport().get_report()
    input(u"下载完成")
