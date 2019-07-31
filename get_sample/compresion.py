# import os
# import shutil
# import datetime
# import configparser
# from subprocess import check_output, SubprocessError
#
#
# class Compression:
#
#     def __init__(self):
#         self.set_path = r"C:\Users\hewen\Desktop\setting.ini"
#         self.path_rar = self.get_setting(self.set_path, "winrar", "path")
#         self.path_7z = self.get_setting(self.set_path, "7-zip", "path")
#         self.password = self.get_setting(self.set_path, "main", "password")
#         self.failed_folder = self.get_failed_folder()
#
#     @staticmethod
#     def get_setting(set_file, section, option):
#         con = configparser.ConfigParser()
#         try:
#             con.read(set_file)
#             result = con.get(section, option)
#             return result
#         except configparser.NoSectionError as e:
#             with open("Error.log", "a+")as file:
#                 file.write(f"{datetime.datetime.now()}:没有配置文件或Section--{e}")
#         except configparser.NoOptionError as e:
#             with open("Error.log", "a+")as file:
#                 file.write(f"{datetime.datetime.now()}:没有配置文件或Option--{e}")
#
#     def get_failed_folder(self):
#         file_path = self.get_setting(self.set_path, "failed", "path")
#         if os.path.exists(file_path) is False:
#             os.makedirs(file_path)
#         return file_path
#
#     def de(self, file_input):
#         dir_path = os.path.dirname(file_input)
#         command_dict = {
#             "rar": {
#                 "path": self.path_rar,
#                 "command": f"rar e -p{self.password} \"{file_input}\" \"{dir_path}\" -y"},
#             "zip": {
#                 "path": self.path_7z,
#                 "command": f"7z e -tzip -p{self.password} \"{file_input}\" -o\"{dir_path}\" -y"},
#             ".gz": {
#                 "path": self.path_7z,
#                 "command": f"7z e -tgzip -p{self.password} \"{file_input}\" -o\"{dir_path}\" -y"},
#             ".7z": {
#                 "path": self.path_7z,
#                 "command": f"7z e -t7z -p{self.password} \"{file_input}\" -o\"{dir_path}\" -y"}
#         }
#
#         try:
#             os.chdir(command_dict[file_input[-3:]]["path"])
#             check_output(command_dict[file_input[-3:]]["command"], shell=True)
#             os.remove(file_input)
#             return True
#         except SubprocessError as e:
#             print(e)
#         except KeyError:
#             pass
#
#     def co(self, file_path, password="infected"):
#         os.chdir(self.path_rar)
#         result_path = file_path + "[infected].rar"
#         command = f"rar a -ep -p{password} \"{result_path}\" \"{file_path}\""
#         try:
#             check_output(command, shell=True)
#             return result_path
#         except SubprocessError as e:
#             print(e)
#             return False
#
#
# if __name__ == "__main__":
#     input_folder = r"C:\Users\hewen\Desktop\11"
#     # for i in os.listdir(input_folder):
#     #     ii = os.path.join(input_folder, i)
#     #     Compression().de(ii)
#     Compression().co(input_folder)
#
