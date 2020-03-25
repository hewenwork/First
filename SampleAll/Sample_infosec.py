from First.SampleAll.InitFile import *


def sample_infosec():
    url = "https://infosec.cert-pa.it/analyze/"
    try:
        sample_dict = {}
        response = session.get(url + "submission.html").text
        md5_list = re.findall(f"<td>{download_date} .*</td>\n.*\n.*<td><a href=\"/analyze/(.*).html\">", response)
        if len(md5_list) == 0:
            return False, "has`t data"
        for sample_md5 in md5_list:
            sample_response = session.get(url + sample_md5 + ".html").text
            link = re.findall(r"rel=\"nofollow\">.*?\.(.*?)</span><span class", sample_response)[0]
            sample_url = "http://" + link.strip("[").strip("]")
            sample_info = {
                "sample_path": os.path.join(sample_dir, sample_md5 + ".vir"),
                "sample_url": sample_url
            }
            sample_dict.update({sample_md5: sample_info})
        return True, sample_dict
    except Exception as e:
        return False, e


if __name__ == "__main__":
    print(sample_infosec())
