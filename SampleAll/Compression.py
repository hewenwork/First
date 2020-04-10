import os
import chardet
from subprocess import check_output


def encoding(string):
    if type(string) is bytes:
        return chardet.detect(string)["encoding"]
    if type(string) is str and os.path.exists(string):
        try:
            with open(string, "rb")as file:
                return chardet.detect(file.read())["encoding"]
        except Exception as e:
            return e


def extract(file_path, pwd="infected"):
    # Determine if the file exists
    if os.path.exists(file_path) is False:
        return f"File isn`t exists: {file_path}."
    # Determine if the file is a compressed file supported by 7z
    try:
        command = f"7z t \"{file_path}\" -p{pwd}"
        result = check_output(command, shell=True)
        result_string = result.decode(encoding(result))
        if "Everything is Ok" in result_string:
            dist_dir = os.path.dirname(file_path)
            extract_command = f"7z e -y -aot -p{pwd} \"{file_path}\" -o\"{dist_dir}\""
            check_output(extract_command, shell=True)
            return f"{file_path} has extract over."
        else:
            return "File error"
    except Exception as e:
        return f"Command error: {e}."


def archive(file_path, dist_path, pwd="infected"):
    if os.path.exists(file_path) is False:
        return False, "file don`t exists"
    try:
        command = f"rar a -ep -p{pwd} -id[c,d,p,q] -y \"{dist_path}\" \"{file_path}\""
        check_output(command, shell=True)
        return True, "compression successful"
    except Exception as e:
        return False, f"compression error: {e}"


if __name__ == "__main__":
    test_path = r"G:\AutoCollect\2020-03-25\a.rar"
    print(extract(test_path))
