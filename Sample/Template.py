from chardet import detect
from requests_html import HTMLSession
from datetime import datetime, timedelta
from subprocess import check_output, SubprocessError

class CMD:

    @staticmethod
    def archive(file_path, **kwargs):
        pass

    @staticmethod
    def extract(file_path, **kwargs):
        pass

    @staticmethod
    def execute(command):
        try:
            output = check_output(command, shell=False)
            encoding = detect(output).setdefault("encoding")
            out = output.decode(encoding=encoding)
        except SubprocessError as e:
            return e
        except LookupError as e:
            return e


class Sample:

    def __init__(self, **kwargs):
        session = HTMLSession()
        url = ""
        date = kwargs.setdefault("date", datetime.today() - timedelta(days=1))

    def __call__(self):
        return "12"


class Run:

    def __init__(self):
        sample_list = Sample().__call__()
        print(sample_list)


if __name__ == "__main__":
    Run()
    print(detect("".encode()))
    print("asd".encode().decode(encoding="0.0"))