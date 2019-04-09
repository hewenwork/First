from contextlib import closing

import faker
import requests

finally_code = False
num = 0
def tt():
    global finally_code
    while finally_code == False:
        headers = {"User-Agent": faker.Faker().user_agent()}
        session = requests.session()
        session.headers.update(headers)
        try:
            with closing(session.get("http://m.mp4se.net/20190103/YtHRBNHO/index.m3u8", stream=True)) as response:
                chunk_size = 1024  # 单次请求最大值
                content_size = int(response.headers['content-length'])  # 内容体总大小
                data_count = 0
                with open(r"C:\Users\hewen\Desktop\auto.mp4", "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        data_count = data_count + len(data)
                        now_jd = (data_count / content_size) * 100
                        print("\r 文件下载进度：%d%%(%d/%d)" % (now_jd, data_count, content_size), end=" ")
                        finally_code = True
        except:
            global num
            print(num)
            num += 1
            if num >= 400:
                finally_code = True

tt()

