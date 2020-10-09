from enum import Enum
from time import time
from ssdeep import compare
from chardet import detect


class Ru:

    def __init__(self, file_path):
        all_ssd_dict = self.get_all_ssd_dict(file_path)
        sort_ssd_dict = self.sort_ssd_dict_list(all_ssd_dict)
        for i, j in sort_ssd_dict.items():
            print(i, len(j))
        result_file_path = file_path + ".ok.db"
        # for ssd_index, sort_ssd_list in sort_ssd_dict.items():
        #     self.write_result(result_file_path, sort_ssd_list, all_ssd_dict)
        self.write_result(result_file_path, sort_ssd_dict["12288"], all_ssd_dict)

    def write_result(self, result_file_path, sort_ssd_list, all_ssd_dict):
        print(len(sort_ssd_list))
        file = open(result_file_path, "a+", encoding="utf-8")
        result = self.compare_ssd_list(sort_ssd_list)
        ssd_list = [all_ssd_dict[ssd] for ssd in result]
        list(map(file.write, ssd_list))
        file.close()

    @staticmethod
    def get_all_ssd_dict(file_path: str):
        with open(file_path, "rb")as file:
            encoding = detect(file.read())["encoding"]
        with open(file_path, "r", encoding=encoding)as file:
            line_dict = {line.split(",")[-1].strip("\n"): line for line in file.readlines()}
        return line_dict

    @staticmethod
    def get_sort_ssd_dict_by_index(ssd_dict: dict):
        new_dict = {}
        for ssd in ssd_dict:
            ssd_index = ssd.split(":")[0]
            if ssd_index not in new_dict:
                new_dict[ssd_index] = [ssd]
            else:
                new_dict[ssd_index].append(ssd)
        return new_dict

    @staticmethod
    def compare_ssd_to_ssd_list(ssd, ssd_list):
        for compare_ssd in ssd_list:
            try:
                result = int(compare(ssd, compare_ssd))
            except:
                pass
            else:
                ssd_list.remove(compare_ssd) if result >= 93 else None
        return ssd_list

    def compare_ssd_list(self, ssd_list):
        new_ssd_list = []
        while True:
            if not ssd_list:
                break
            ssd = ssd_list[0]
            new_ssd_list.append(ssd)
            ssd_list.remove(ssd)
            ssd_list = self.compare_ssd_to_ssd_list(ssd, ssd_list)
            print("\r", len(new_ssd_list), end="")
        return new_ssd_list

    @staticmethod
    def sort_ssd_dict_list(ssd_dict):
        new_dict = {}
        for ssd in ssd_dict:
            ssd_index = ssd.split(":")[0]
            if ssd_index not in new_dict:
                new_dict[ssd_index] = [ssd]
            else:
                new_dict[ssd_index].append(ssd)
        return new_dict


def test_list(ssd_list):
    have_ssd = []
    for i in range(len(ssd_list)):
        ssd = ssd_list[i]
        compare_list = ssd_list[i + 1:]
        ssd_list = test_com(ssd, compare_list)


def test_com(ssd, ssd_list: list):
    for compare_ssd in ssd_list:
        try:
            result = compare(ssd, compare_ssd)
            if result >= 93:
                ssd_list.remove(compare_ssd)
        except:
            pass
    return ssd_list


if __name__ == "__main__":
    ssd_path = r"C:\Users\hewen\Desktop\0909.db"
    Ru(ssd_path)
