import os
import asyncio
import time

import requests


class Down:

    def __init__(self):
        self.url = "http://update.iobit.com/dl/test/ASCv13.0.0.100_Setup_Beta_20190806_1938.exe"
        self.file = open(r"C:\Users\hewen\Desktop\aa.exe", "wb")
        self.loop = asyncio.get_event_loop()
        self.get_total_size()
        self.file.close()
        self.loop.close()

    def get_total_size(self):
        response = requests.get(self.url, stream=True)
        total_size = int(response.headers["Content-Length"])
        start_size = 0
        chunk_size = 1024 * 1024
        task = []
        for i in range(int(total_size / chunk_size) + 1):
            end_size = chunk_size + start_size
            task.append(self.loop.create_task(self._star(start_size, end_size)))
            start_size = end_size + 1
        self.loop.run_until_complete(asyncio.wait(task))

    async def _star(self, start_size, end_size):
        self.file.seek(start_size, 0)
        headers = {"range": f"bytes={start_size}-{end_size}"}
        chunk = requests.get(self.url, stream=True, headers=headers)
        self.file.write(chunk.content)
        self.file.flush()
        print(start_size)


def tt():
    url = "http://update.iobit.com/dl/test/ASCv13.0.0.100_Setup_Beta_20190806_1938.exe"
    file = open(r"C:\Users\hewen\Desktop\ab.exe", "wb")
    file.write(requests.get(url).content)
    file.close()


if __name__ == "__main__":
    s = time.time()
    Down()
    print(time.time() - s)
    ss = time.time()
    tt()
    print(time.time() - ss)
