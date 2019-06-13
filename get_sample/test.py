from get_sample.sample_all import start
from get_sample.compresion import Compression
from base.base_func import Base

download_folder = r"C:\Users\hewen\Desktop\MyTest\2019-06-12"
Compression().auto_de_folder(download_folder)
list(map(Base.rename_file, Base.get_list(download_folder)))
final_file = Compression().co_rar(download_folder)
Base.copy_file(final_file, r"\\192.168.1.39\f\Auto")
