import os
import time
import asyncio
import aiohttp
import requests
from faker import Faker


class DownUp:

    def __new__(cls, *args, **kwargs):
        cls.user_desk = os.path.join(os.path.expanduser("~"), "Desktop")
        cls.headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": Faker().user_agent()
        }
        cls.chunk_size = 1024 * 1024
        cls.task = []
        return object.__new__(cls)

    def __init__(self, url, auth=None):
        self.url = url
        file_name = self.url.split("/")[-1]
        file_path = r"{}\{}".format(self.user_desk, file_name)
        self.file = open(file_path, "wb")
        response = requests.get(self.url, stream=True, headers=self.headers, auth=auth)
        if "Accept-Ranges" in response.headers.keys():
            aiohttp.BasicAuth = auth
            self.total_size = int(response.headers["Content-Length"])
            self.chunk_num = int(self.total_size / self.chunk_size) + 1
            self.loop = asyncio.get_event_loop()
            self.loop.run_until_complete(self.get_total_size())
            self.loop.close()
        else:
            self.alone(self.url)
        self.file.close()

    async def get_total_size(self):
        async with aiohttp.ClientSession() as session:
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
        except Exception as e:
            print(e)
            return


if __name__ == "__main__":
    download_url = "http://update.iobit.com/dl/imf7/bd/bdfull-190830.exe"
    DownUp(download_url)
