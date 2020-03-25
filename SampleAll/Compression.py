import os
from subprocess import check_output


def compression(file_path, dist_path, pwd="infected"):
    if os.path.exists(file_path) is False:
        return False, "file don`t exists"
    try:
        command = f"rar a -ep -p{pwd} -id[c,d,p,q] -y \"{dist_path}\" \"{file_path}\""
        check_output(command, shell=True)
        return True, "compression successful"
    except Exception as e:
        return False, f"compression error: {e}"


def decompression(file_path, pwd="infected"):
    if os.path.exists(file_path) is False:
        return False, "File don`t exists"
    file_type = file_path[-3:]
    dist_path = file_path.split(".")[0] + ".vir"
    type_command = {
        "rar": f"rar e -p{pwd} -y \"{file_path}\" \"{dist_path}\"",
        "7z": f"7z e -p{pwd} -y \"{file_path}\" -so > \"{dist_path}\"",
        "zip": f"7z e -p{pwd} -y \"{file_path}\" -so > \"{dist_path}\"",
        ".gz": f"7z e -p{pwd} -y \"{file_path}\" -so > \"{dist_path}\"",
    }
    if file_type in type_command is False:
        return False, "File isn`t compression"
    try:
        command = type_command[file_type]
        check_output(command, shell=True)
        os.remove(file_path)
        return True, "Decompression successful"
    except Exception as e:
        return False, f"Decompression Error: {e}"
