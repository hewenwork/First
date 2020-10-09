from ssdeep import compare
from chardet import detect


def log(function):
    def run(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = False
            print(e)
        return result

    return run


@log
def get_all_ssd_dict(file_path: str):
    with open(file_path, "rb")as file:
        encoding = detect(file.read())["encoding"]
    with open(file_path, "r", encoding=encoding)as file:
        line_dict = {line.split(",")[-1].strip("\n"): line for line in file.readlines()}
    return line_dict


def compare_ssd_to_ssd_list(ssd, ssd_list):
    for compare_ssd in ssd_list:
        try:
            result = int(compare(ssd, compare_ssd))
            if  result>= 93:
                ssd_list.remove(compare_ssd)
        except:
            pass
            # ssd_list.remove(compare_ssd)
            # print(ssd, compare_ssd)
    return ssd_list


def cs(ssd_list):
    new_ssd_list =[]
    while True:
        if not ssd_list:
            break
        ssd = ssd_list[0]
        new_ssd_list.append(ssd)
        ssd_list.remove(ssd)
        ssd_list = compare_ssd_to_ssd_list(ssd, ssd_list)
    return new_ssd_list

def sort_ssd_dict_list(ssd_dict):
    new_dict = {}
    for ssd in ssd_dict:
        ssd_index = ssd.split(":")[0]
        if ssd_index not in new_dict:
            new_dict[ssd_index] = [ssd]
        else:
            new_dict[ssd_index].append(ssd)
    return new_dict
#
# ssd_path = r"C:\Users\hewen\Desktop\SsDeepa.db"
# all_ssd_dict = get_all_ssd_dict(ssd_path)
# sort_ssd_dict = sort_ssd_dict_list(all_ssd_dict)
# with open(r"C:\Users\hewen\Desktop\SsDeepaaa.db", "w", encoding="utf-8")as aa:
#     for a, j in sort_ssd_dict.items():
#         print(a, len(j))
#         result = cs(j)
#         for k in result:
#             aa.write(all_ssd_dict[k])
#         break

a = "768:uTERvKYRgrpRqt6LuSBQ6qRD549AFlgsQAygevZJH:FKsgFRqtAuS66q/49AwsQAygevZ1"
b = "768:uTERvKYRgrpRqt6LuSBQ6qRD549AFlgsQAygevZz:FKsgFRqtAuS66q/49AwsQAygevZz"
print(compare(a, b))