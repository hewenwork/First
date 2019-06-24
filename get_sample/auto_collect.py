import datetime
from base import Base
from sample_all import start
from compresion import Compression


class Auto:
    def __init__(self, mode):
        if mode == "1":
            self.start_download()
        elif mode == "2":
            while True:
                date_now = datetime.datetime.now().strftime("%H:%M:%S")
                print("\rNow time: %s  Start time: 08:00:00" % date_now, end="")
                if date_now == "08:00:00":
                    print("Start Download")
                    self.start_download()
        else:
            print("Pls input the Num of Download Mode")

    @staticmethod
    def start_download():
        download_folder = start()
        Compression().auto_de_folder(download_folder)
        list(map(Base.rename_file, Base.get_list(download_folder)))
        final_file = Compression().co_rar(download_folder)
        Base.copy_file(final_file, r"\\192.168.1.39\f\Auto")


if __name__ == "__main__":
    download_mode = input("Choose Download Mode:\nDownload Once: 1\nDownload Everyday: 2\nMode:")
    Auto(download_mode)
