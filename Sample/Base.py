from datetime import datetime
from subprocess import check_output
from os import path


def log(function):
    def run(*args, **kwargs):
        function_name = function.__name__
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = "function: {}, Exception:{}".format(function_name, e)
        file_path = "Base-{}.log".format(datetime.today().strftime("%Y%m%d"))
        line = "{}: {}\n".format(datetime.today(), result)
        with open(file_path, "a+")as file:
            file.write(line)
        return result

    return run


@log
def execute_cmd(command: str = None):
    output = check_output(command, shell=False)
    out = output.decode()
    return out


@log
def archive(file_path: str, **kwargs):
    assert file_path is not None, "file_path is None"
    password = kwargs.setdefault("password", "infected")
    archive_path = kwargs.setdefault("archive_path")
    if archive_path is None:
        file_dir = path.dirname(file_path)
        archive_dir = kwargs.setdefault("archive_dir", file_dir)
        file_name = path.basename(file_path).split(".")[0]
        archive_name = kwargs.setdefault("archive_name", f"[{password}]{file_name}.zip")
        archive_path = path.join(archive_dir, archive_name)
    if ".rar" in archive_path:
        attr_mode = "rar a -ep -p{} -y".format(password)
        attr_archive = "\"{}\"".format(archive_path)
        attr_file = "\"{}\"".format(file_path)
    else:
        attr_mode = "7z a -ep -p{} -y".format(password)
        attr_archive = "\"{}\"".format(archive_path)
        attr_file = "\"{}\\*\"".format(file_path) if path.isdir(file_path) else "\"{}\"".format(file_path)
    command = attr_mode + attr_archive + attr_file
    execute_result = execute_cmd(command)
    return True if "Ok" in execute_result else execute_result


@log
def extract(archive_path, dist_dir, password="infected"):
    command = "7z e \"{}\" -o\"{}\" -p{} -y -r".format(archive_path, dist_dir, password)
    output = check_output(command, shell=False)
    out = output.decode()
    return True if "Ok" in out else out


# def cmd(command, **kwargs):
#     file_path = kwargs.setdefault("file_path")
#     dist_dir = kwargs.setdefault("dist_dir")
#     dist_path = kwargs.setdefault("dist_path")
#     command_dict = {
#         "copy": f"copy /y \"{file_path}\" \"{dist_dir}\"",
#         "move": f"move /y \"{file_path}\" \"{dist_dir}\"",
#         "rename": f"rename /y \"{file_path}\" \"{dist_path}\"",
#         "delete": f"RD /S /Q \"{file_path}\"" if path.isdir(file_path) else f"DEl /Q \"{file_path}\""
#     }
#     command = command_dict[command]
#     output = check_output(command, shell=False)
#     encoding = detect(output)["encoding"]
#     out = output.decode(encoding=encoding)
#     return out
from ssdeep import compare
a = "12288:S4fmuV/2SlI1MCAHab5I0WozQsmknY87Z1EPclMkc9A7Z2S:S42DMCA6b5fWQmknY87LEPcl9nl/"
b = "12288:d4fmuV/2SlI1MCAHab5I0WozQsmknY87Z1EPclMkc9A7Z2J:d42DMCA6b5fWQmknY87LEPcl9nlY"
print(compare(a, b))