import os
import gzip
import shutil
import winreg
import zipfile


class all_func():

    def __init__(self):
        self.user_path = os.path.expanduser("~")
        self.local_rar_path = self.get_local_rar_path()
        self.local_z7_path = self.get_local_z7_path()

    def get_local_rar_path(self):
        try:
            rar_key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WinRAR")
            self.local_rar_path = os.path.dirname(winreg.QueryValueEx(rar_key, r"exe64")[0])
        except:
            cloud_rar_path = r"C:\Program Files\WinRAR"
            self.local_rar_path = os.path.join(self.user_path, "AppData\Local\Temp\RAR")
            try:
                shutil.copytree(cloud_rar_path, self.local_rar_path)
            except:
                print("error: copy cloud RAR to local failed ")
        return self.local_rar_path

    def get_local_z7_path(self):
        try:
            z7_key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\7-Zip")
            self.local_z7_path = os.path.dirname(winreg.QueryValueEx(z7_key, r"Path")[0])
        except:
            cloud_z7_path = r"C:\Program Files\7-Zip"
            self.local_z7_path = os.path.join(self.user_path, "AppData\Local\Temp\z7")
            try:
                shutil.copytree(cloud_z7_path, self.local_z7_path)
            except:
                print("error: copy cloud 7z to local failed ")
        return self.local_z7_path

    def gz_func(self, gz_file_path):
        dir_path = os.path.dirname(gz_file_path)
        failed_dir_path = os.path.join(dir_path, "Failed")
        try:
            with open(gz_file_path[:-3], "wb")as de_gz_file:
                de_gz_file.write(gzip.GzipFile(gz_file_path).read())
        except:
            file_name = gz_file_path.split("\\")[-1]
            if os.path.exists(failed_dir_path) == False:
                os.makedirs(failed_dir_path)
            if os.path.exists(os.path.join(failed_dir_path, file_name)) == False:
                shutil.move(gz_file_path, failed_dir_path)
            else:
                os.remove(os.path.join(failed_dir_path, file_name))
                shutil.move(gz_file_path, failed_dir_path)

    def rar_func(self, rar_file_path, password="infected"):
        dir_path = os.path.dirname(rar_file_path)
        failed_dir_path = os.path.join(dir_path, "Failed")
        os.chdir(self.local_rar_path)
        result = os.popen("rar e -p%s -y \"%s\" %s" % (password, rar_file_path, dir_path))
        if "OK" not in result:
            file_name = rar_file_path.split("\\")[-1]
            if os.path.exists(failed_dir_path) == False:
                os.makedirs(failed_dir_path)
            if os.path.exists(os.path.join(failed_dir_path, file_name)) == False:
                shutil.move(rar_file_path, failed_dir_path)
            else:
                os.remove(os.path.join(failed_dir_path, file_name))
                shutil.move(rar_file_path, failed_dir_path)

    def z7_func(self, z7_file_path, password="infected", z7="e"):
        dir_path = os.path.dirname(z7_file_path)
        failed_dir_path = os.path.join(dir_path, "Failed")
        os.chdir(self.local_z7_path)
        result = os.popen("7z %s -p%s -y \"%s\" -o%s" % (z7, password, z7_file_path, dir_path)).read()
        if "Everything is Ok" not in result:
            file_name = z7_file_path.split("\\")[-1]
            if os.path.exists(failed_dir_path) == False:
                os.makedirs(failed_dir_path)
            if os.path.exists(os.path.join(failed_dir_path, file_name)):
                os.remove(os.path.join(failed_dir_path, file_name))
                shutil.move(z7_file_path, failed_dir_path)
            else:
                shutil.move(z7_file_path, failed_dir_path)

    def zip_func(self, zip_file_path, password="infected"):
        dir_path = os.path.dirname(zip_file_path)
        failed_dir_path = os.path.join(dir_path, "Failed")
        try:
            with zipfile.ZipFile(zip_file_path, "r")as zip_file:
                zip_file.setpassword(password.encode("utf-8"))
                for son_file_name in zip_file.namelist():
                    print(son_file_name.encode("cp437").decode("utf-8"))
                # zip_file.extractall(dir_path)
        except:
            file_name = zip_file_path.split("\\")[-1]
            if os.path.exists(failed_dir_path)==False:
                os.makedirs(failed_dir_path)
            if os.path.exists(os.path.join(failed_dir_path, file_name)):
                os.remove(os.path.join(failed_dir_path, file_name))
                shutil.move(zip_file_path, failed_dir_path)
            else:
                shutil.move(zip_file_path, failed_dir_path)


all_func().z7_func(r"C:\Users\hewen\Desktop\auto\Win32 API大全.zip", z7="x -tzip")
