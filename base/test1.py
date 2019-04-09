import os
import re
import time
from contextlib import closing
import faker
import requests


num = 0


def write_sample(session, sample_name, sample_download_url, auth=None):
    file_download_path = sample_name
    if os.path.exists(file_download_path) == False:
        try:
            with closing(session.get(sample_download_url, stream=True, auth=auth)) as response:
                chunk_size = 1024  # 单次请求最大值
                content_size = int(response.headers['content-length'])  # 内容体总大小
                data_count = 0
                with open(file_download_path, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        data_count = data_count + len(data)
                        now_jd = (data_count / content_size) * 100
                        print("\r 文件下载进度：%d%%(%d/%d) - %s" % (now_jd, data_count, content_size, file_download_path),end=" ")
                        return True
        except:
            return False



def get_img(url_path):
    global finally_code
    while finally_code == False:
        # time.sleep(1)
        url = "http://www.5bnbn.org/art/html/%s.html" % url_path
        headers = {"User-Agent": faker.Faker().user_agent()}
        session = requests.session()
        session.headers.update(headers)
        try:
            with closing(session.get(url))as respone:
                img_list = re.findall("<img src=\"(.*?)\" border", respone.text)
                for img_file in img_list:
                    print(img_file)
                    file_name = os.path.join(r"C:\Users\hewen\Desktop\auto", img_file.split("/")[-1])
                    with open(file_name, "wb")as file:
                        try:
                            # finally_code = write_sample(session, file_name, img_file)
                            with open(file_name, "wb")as file:
                                file.write(session.get(img_file).content)
                                finally_code = True
                        except:
                            os.remove(img_file)
        except:
            global num
            num += 1
            if num >= 66:
                finally_code = True
                with open(r"C:\Users\hewen\Desktop\auto\failed.txt", "a+")as file:
                    file.writelines("%s\n"% url)


for i in range(400, 670):
    finally_code = False
    print(i)
    get_img(i)

