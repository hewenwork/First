import os
import time
import asyncio
import aiohttp
import requests
from faker import Faker


class DownUp:

    def __new__(cls, *args, **kwargs):
        cls.user_desk = os.path.join(os.path.expanduser("~"), "Desktop")
        cls.start_time = time.time()
        cls.headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": Faker().user_agent()
        }
        return object.__new__(cls)

    def __init__(self, aa, auth=None):
        self.url = aa
        file_name = "aaa.json"
        self.file = open(r"{}\{}".format(self.user_desk, file_name), "wb")
        response = requests.get(self.url, stream=True, headers=self.headers, auth=auth)
        if "Accept-Ranges" in response.headers.keys():  # ["Accept-Ranges"] == "bytes":
            aiohttp.BasicAuth = auth
            print(response.status_code)
            self.task = []
            self.total_size = int(response.headers["Content-Length"])
            self.chunk_size = 1024 * 1024
            self.chunk_num = int(self.total_size / self.chunk_size) + 1
            self.loop = asyncio.get_event_loop()
            self.loop.run_until_complete(self.get_total_size())
            self.loop.close()
        else:
            self.alone(self.url)
        self.file.close()
        print(time.time() - self.start_time)

    async def get_total_size(self):
        async with aiohttp.ClientSession() as session:
            # session.auth = ("f_yunwing1", "9kkSkk3dSd")
            start_size = 0
            for i in range(self.chunk_num):
                end_size = self.chunk_size + start_size
                if self.chunk_num - i == 1:
                    end_size = self.total_size
                self.task.append(self.loop.create_task(self._star(start_size, end_size, session)))
                start_size = end_size + 1
            await asyncio.wait(self.task)

    async def _star(self, start_size, end_size, session):
        self.headers["range"] = f"bytes={start_size}-{end_size}"
        async with session.get(self.url, headers=self.headers)as chunk:
            self.continue_download = False
            content = await chunk.read()
            self.file.seek(start_size, 0)
            self.file.write(content)
            self.file.flush()

    def alone(self, url):
        try:
            with requests.get(url).content as content:
                self.file.write(content)
            print(time.time() - self.start_time)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    download_url = "http://backup.iobit.com.php56-23.dfw3-2.websitetestlink.com/bugReport/export.php?action=bugreport_today&name=iu_bugreport_v2"
    DownUp(download_url)
    # with open(r"C:\Users\hewen\Desktop\virussign.com_20190806_Free.zip", "rb")as file:
    #     a = file.read(11111)
    #     print(a)
