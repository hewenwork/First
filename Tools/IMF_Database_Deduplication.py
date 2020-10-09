from chardet import detect
from os import path, remove
from threading import Thread
from re import match, findall
from tkinter import Tk
from tkinter.ttk import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename

sig_special = """000000000000000000000000D0020000010053007400720069006E006700460069006C00650049006E0066006F000000AC020000010030003400300039003000340062003000000018000000010043006F006D006D0065006E00740073000000
010053007400720069006E006700460069006C00650049006E0066006F0000007801000001003000300030003000300034006200300000002C0002000100460069006C0065004400650073006300720069007000740069006F006E0000000000
068B7C2414418D14383BC2891673108BD02BD1408A128850FF8B163BC272F08B44241003C7894424108BF8EB0B8BCEE8F7FBFFFF84C0741C3B7C24280F82ABFDFFFF8B44242C89385F5E5DB0015B83C414C208005F5E5D32C05B83C414C20800
078B1E83EEFC11DB72BE01DB75078B1E83EEFC11DB11C901DB73EF75098B1E83EEFC11DB73E483C10281FD00FBFFFF83D1028D142F83FDFC760E8A02428807474975F7E942FFFFFF8B0283C204890783C70483E90477F101CFE92CFFFFFF5E89
0881E2FF0000000BCA8B560883C2F8894E0C8BCA89560883F90873CE8B7E088B560CB9080000002BCF03FBD3EAB918000000897E082BCB81E2FFFFFF00D3EA33C956E803FFFFFF8A8C30064044005E8B44241403CA03C1894424148A86640200
249568CD40008BFF78CD400080CD40008CCD4000A0CD40008B45085E5FC9C3908A0688078B45085E5FC9C3908A0688078A46018847018B45085E5FC9C38D49008A0688078A46018847018A46028847028B45085E5FC9C3908D7431FC8D7C39FC
3000300034006200300000002C0002000100460069006C0065004400650073006300720069007000740069006F006E000000000020000000300008000100460069006C006500560065007200730069006F006E000000000030002E0030002E00
11C901DB73EF75098B1E83EEFC11DB73E483C10281FD00F3FFFF83D1018D142F83FDFC760F8A02428807474975F7E963FFFFFF908B0283C204890783C70483E90477F101CFE94CFFFFFF5E89F7B91A0000008A07472CE83C0177F7803F0075F2
4163636573733D2266616C7365222F3E0D0A2020202020203C2F72657175657374656450726976696C656765733E0D0A202020203C2F73656375726974793E0D0A20203C2F7472757374496E666F3E0D0A3C2F617373656D626C793E0D0A0000
44494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E475858504144
494E47585850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444
50414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4700000000000000000000000000000000
5850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E47585850414444494E4750414444494E4758
636573733D2766616C736527202F3E0D0A2020202020203C2F72657175657374656450726976696C656765733E0D0A202020203C2F73656375726974793E0D0A20203C2F7472757374496E666F3E0D0A3C2F617373656D626C793E0D0A000000
6400750063007400560065007200730069006F006E00000030002E0030002E0030002E003000000038000800010041007300730065006D0062006C0079002000560065007200730069006F006E00000030002E0030002E0030002E0030000000
6564457865637574696F6E4C6576656C206C6576656C3D226173496E766F6B6572222075694163636573733D2266616C7365223E3C2F726571756573746564457865637574696F6E4C6576656C3E0D0A2020202020203C2F7265717565737465
726D696E61746550726F636573730000A90147657443757272656E7450726F63657373003E04556E68616E646C6564457863657074696F6E46696C74657200001504536574556E68616E646C6564457863657074696F6E46696C74657200D102
7368000047657444430000004C6F61645573657250726F66696C65570000566572517565727956616C75655700004674704F70656E46696C6557000074696D6547657454696D6500000000000000000000000000000000000000000000000000
7400720069006E006700460069006C00650049006E0066006F0000007801000001003000300030003000300034006200300000002C0002000100460069006C0065004400650073006300720069007000740069006F006E000000000020000000
746564457865637574696F6E4C6576656C3E0D0A2020202020203C2F72657175657374656450726976696C656765733E0D0A202020203C2F73656375726974793E0D0A20203C2F7472757374496E666F3E0D0A3C2F617373656D626C793E5041
865B0200008D4E10E883FCFFFF3D0001000073138B0E88018B0E4147890E897C2410E9290200003DD00200000F83130200000500FFFFFF8BE883E007C1ED038D500283F807895424140F85940000008D8EA0000000E836FCFFFF8B4E0833DB56
8B54240C8B4C240485D2744733C08A442408578BF983FA04722DF7D983E10374082BD18807474975FA8BC8C1E00803C18BC8C1E01003C18BCA83E203C1E9027406F3AB85D274068807474A75FA8B4424085FC38B442404C3FF25
8B54240C8B4C240485D2744F33C08A442408578BF983FA047231F7D983E103740C2BD1880783C70183E90175F68BC8C1E00803C18BC8C1E01003C18BCA83E203C1E9027406F3AB85D2740A880783C70183EA0175F68B4424085FC38B442404C3
C4048BF856E89E0F00008B461083C40450E8B20E000083C40485C07D0F83CFFFC7460C000000008BC75F5EC38B461C85C0741050E81F02000083C404C7461C000000008BC7C7460C000000005F5EC3909090909090909090558BEC6AFF68F871
C454030000C38B042481C454030000C210000001020304050607080A0C0E1014181C202830384050607080A0C0E00000000000000000010101010202020203030303040404040505050500000000010102020303040405050606070708080909
EB109090909090908A064688074701DB75078B1E83EEFC11DB72EDB80100000001DB75078B1E83EEFC11DB11C001DB73EF75098B1E83EEFC11DB73E431C983E803720DC1E0088A064683F0FF747489C501DB75078B1E83EEFC11DB11C901DB75
EEFC11DB11C975204101DB75078B1E83EEFC11DB11C901DB73EF75098B1E83EEFC11DB73E483C10281FD00F3FFFF83D1018D142F83FDFC760F8A02428807474975F7E963FFFFFF908B0283C204890783C70483E90477F101CFE94CFFFFFF5E89
F8000007F800001FF800007FF80001FFF80001FFF80001FFF80001FFF80001FFF80001FFF80001FFF80001FFF80001FFF80001FFF80001FFF8003FFFF803FFFFF83FFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FF80001FF8000007F800001FF800007FF80001FFF80001FFF80001FFF80001FFF80001FFF80001FFF80001FFF80001FFF80001FFF80001FFF80001FFF8003FFFF803FFFFF83FFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
"""
sig_special_list = sig_special.split("\n")


def check_file(file_path: str, file_type: str):
    try:
        with open(file_path, "rb")as file:
            content = file.read()
        encoding = detect(content)["encoding"]
    except Exception as e:
        return "Get File Encoding Exception: {}".format(e)
    file_ok_path = file_path + "_ok.db"
    file_del_path = file_path + "_del.db"
    try:
        with open(file=file_path, mode="r", encoding=encoding)as file:
            content = file.readlines()
    except Exception as e:
        return e
    dict_md5 = {
        "re_match_line": r"^[\w\s\S]*?,[a-z0-9]{32}?,\d*?$",
        "re_match_key": r"^[\w\s\S]*?,([a-z0-9]*?),\d*?$"
    }
    dict_sig = {
        "re_match_line": r"^[\w\s\S]*?,\d*?,[A-Z0-9]*?$",
        "re_match_key": r"^[\w\s\S]*?,(\d*?,[A-Z0-9]*?)$"
    }
    dict_sign = {
        "re_match_line": r"^[\w\s\S]*?,[0-9]*?,[a-zA-Z0-9]*?,[0-9]*?,[a-zA-Z0-9]*$",
        "re_match_key": r"^[\w\s\S]*?,([0-9]*?,[a-zA-Z0-9]*?,[0-9]*?,[a-zA-Z0-9]*)$"
    }
    dict_ssdeep = {
        "re_match_line": r"^[\w\s\S]*?,\d*?:.*?:.*?$",
        "re_match_key": r"^[\w\s\S]*?,(\d*?:.*?:.*?$)"
    }
    dict_database_md5 = {
        "re_match_line": r"^\d*?,\d*?,[\w\s\S]*?,[a-z0-9]{32}?,\d*?$",
        "re_match_key": r"^\d*?,\d*?,[\w\s\S]*?,([a-z0-9]*?),\d*?$"
    }
    dict_database_sig = {
        "re_match_line": r"^\d*?,\d*?,[\w\s\S]*?,\d*?,[A-Z0-9]*?$",
        "re_match_key": r"^\d*?,\d*?,[\w\s\S]*?,(\d*?,[A-Z0-9]*?)$"
    }
    dict_database_sign = {
        "re_match_line": r"^\d*?,\d*?,[\w\s\S]*?,[0-9]*?,[a-zA-Z0-9]*?,[0-9]*?,[a-zA-Z0-9]*$",
        "re_match_key": r"^\d*?,\d*?,[\w\s\S]*?,([0-9]*?,[a-zA-Z0-9]*?,[0-9]*?,[a-zA-Z0-9]*)$"
    }
    dict_database_ssdeep = {
        "re_match_line": r"^\d*?,\d*?,[\w\s\S]*?,\d*?:.*?:.*?$",
        "re_match_key": r"^\d*?,\d*?,[\w\s\S]*?,(\d*?:.*?:.*?$)"
    }
    file_type_dict = {
        "md5": dict_md5,
        "sig": dict_sig,
        "sign": dict_sign,
        "ssdeep": dict_ssdeep,
        "database_md5": dict_database_md5,
        "database_sig": dict_database_sig,
        "database_sign": dict_database_sign,
        "database_ssdeep": dict_database_ssdeep
    }
    if file_type not in file_type_dict:
        return "Not match file type re, it support md5, sig, sign"
    re_match_line = file_type_dict[file_type]["re_match_line"]
    re_match_key = file_type_dict[file_type]["re_match_key"]
    re_not_match_list = []
    just_for_sig_special = []
    key_repeat_list = []
    key_dict = {}
    for line in content:
        if match(re_match_line, line):
            key = findall(re_match_key, line)[0]
            if file_type == "sig" or file_type == "database_sig":
                if key in sig_special_list:
                    just_for_sig_special.append(line)
                else:
                    key_dict.update({key: line}) if key not in key_dict else key_repeat_list.append(line)
            else:
                key_dict.update({key: line}) if key not in key_dict else key_repeat_list.append(line)
        else:
            re_not_match_list.append(line)
    with open(file_ok_path, "w+", encoding="utf-8") as file_ok:
        for key, value in key_dict.items():
            file_ok.write(value)
    with open(file_del_path, "w+", encoding="utf-8")as file_del:
        file_del.write("以下内容不符合收录格式:\n") if len(re_not_match_list) != 0 else None
        for line in re_not_match_list:
            file_del.write(line)
        file_del.write("\n\n以下内容重复:\n") if len(key_repeat_list) != 0 else None
        for line in key_repeat_list:
            file_del.write(line)
        file_del.write("\n\n以下内容Sig误报特别大:\n") if len(just_for_sig_special) != 0 else None
        for line in just_for_sig_special:
            file_del.write(line)
    if path.getsize(file_ok_path) == 0:
        remove(file_ok_path)
        remove(file_del_path)
        return "文件错误, 没有找到符合匹配的项目."
    elif path.getsize(file_del_path) == 0:
        remove(file_del_path)
        remove(file_ok_path)
        return "文件处理完成, 没有找到不符合规则或者重复的项目"
    else:
        return "文件处理完成!\n处理完成文件:{}\n错误文件:{}".format(file_ok_path, file_del_path)


def thread_action(function):
    # 回调
    def mu(*args, **kwargs):
        # 多线程
        thread = Thread(target=function, args=args, kwargs=kwargs)
        return thread.start()

    return mu


class UI:
    user_manual = """
    说明:
    1. 点击选择要去除重复的文件, 目前支持MD5, Sig, SigN, Ssd
    2. 项目重复会被删除, 删除的项目保存文件为原文件名加_del.db
    3. 处理完成文件为原文件名加_ok.db
    4. 文件没有重复的数据, 则不会生成任何文件, 提示成功
    5. 去除原理: 
        - 先看整行是否重复
        - 按照数据库格式分割
        - 然后看MD5或特征码(加上偏移量)是否重复
    6. 各个格式规则如下:
    收集的待制作数据库的文件--------------
    MD5格式: 威胁名,MD5,大小
    Sig格式: 威胁名,偏移量,特征码
    SigN格式: 威胁名,偏移量,特征码
    Ssd格式:威胁名,偏移量,特征码:特征码\n 
    数据库中已经制作好的数据解密文件--------
    MD5格式: 数据编号,数据库编号,威胁名,MD5,大小
    Sig格式: 数据编号,数据库编号,威胁名,偏移量,特征码
    SigN格式: 数据编号,数据库编号,威胁名,偏移量1,特征码1,偏移量2,特征码2
    Ssd格式: 数据编号,数据库编号,威胁名,偏移量,特征码:特征码\n 
    """

    def __init__(self):
        self.app = self.main(700, 500)
        button_md5_option = {"text": "收集_MD5", "command": lambda: self.command_all("md5")}
        self.button_md5 = self.button(**button_md5_option)
        button_sig_option = {"text": "收集_Signature", "command": lambda: self.command_all("sig")}
        self.button_sig = self.button(**button_sig_option)
        button_sign_option = {"text": "收集_SignatureN", "command": lambda: self.command_all("sign")}
        self.button_sign = self.button(**button_sign_option)
        button_ssdeep_option = {"text": "收集_SsDeep", "command": lambda: self.command_all("ssdeep")}
        self.button_ssdeep = self.button(**button_ssdeep_option)
        button_md5_database_option = {"text": "数据库_MD5", "command": lambda: self.command_all("database_md5")}
        self.button_md5_database = self.button(**button_md5_database_option)
        button_sig_database_option = {"text": "数据库_Signature", "command": lambda: self.command_all("database_sig")}
        self.button_sig_database = self.button(**button_sig_database_option)
        button_sign_database_option = {"text": "数据库_SignatureN", "command": lambda: self.command_all("database_sign")}
        self.button_sign_database = self.button(**button_sign_database_option)
        button_ssdeep_database_option = {"text": "数据库_Ssdeep", "command": lambda: self.command_all("database_ssdeep")}
        self.button_ssdeep_database = self.button(**button_ssdeep_database_option)
        self.label_information = self.label(text=self.user_manual)
        self.app_grid()
        self.app.mainloop()

    def app_grid(self):
        self.app.update()
        app_width = self.app.winfo_width()
        # app_height = self.app.winfo_height()
        self.label_information.place(x=10, y=10)
        self.button_md5.place(x=int(app_width * 0.8 - 100), y=20, width=150, height=30)
        self.button_sig.place(x=int(app_width * 0.8 - 100), y=60, width=150, height=30)
        self.button_sign.place(x=int(app_width * 0.8 - 100), y=100, width=150, height=30)
        self.button_ssdeep.place(x=int(app_width * 0.8 - 100), y=140, width=150, height=30)
        self.button_md5_database.place(x=int(app_width * 0.8 - 100), y=180, width=150, height=30)
        self.button_sig_database.place(x=int(app_width * 0.8 - 100), y=220, width=150, height=30)
        self.button_sign_database.place(x=int(app_width * 0.8 - 100), y=260, width=150, height=30)
        self.button_ssdeep_database.place(x=int(app_width * 0.8 - 100), y=300, width=150, height=30)

    @staticmethod
    def main(app_width=None, app_height=None):
        app = Tk()
        app_max_width_size, app_max_height_size = app.maxsize()
        app_width = int(app_max_width_size / 3) if app_width is None else app_width
        app_height = int(app_max_height_size / 2) if app_height is None else app_height
        location_x = int((app_max_width_size - app_width) / 2)
        location_y = int((app_max_height_size - app_width) / 2)
        app.geometry("{}x{}+{}+{}".format(app_width, app_height, location_x, location_y))
        app.resizable(False, False)
        app.title("IMF数据库去重工具".center(40))
        return app

    def button(self, **kwargs):
        kwargs.setdefault("text", "this button")
        button_ = Button(self.app, **kwargs)
        return button_

    def label(self, **kwargs):
        kwargs.setdefault("text", "this label")
        label_ = Label(self.app, **kwargs)
        return label_

    @staticmethod
    @thread_action
    def command_all(file_type):
        file_path = askopenfilename()
        if path.exists(file_path) is False:
            return showinfo(title="错误", message="没有选择任何文件")
        result = check_file(file_path, file_type)
        showinfo(title="文件处理结果", message=result)


if __name__ == "__main__":
    UI()
