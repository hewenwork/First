from get_sample.sample_all import start
from get_sample.compresion import Compression
from base.base_func import Base

if __name__ == "__main__":
    download_folder = start()
    Compression().auto_de_folder(download_folder)
    list(map(Base.rename_file, Base.get_list(download_folder)))
    final_file = Compression().co_rar(download_folder)
    Base.copy_file(final_file, r"\\192.168.1.39\f\Auto")
