from First.SampleAll.InitFile import *

url = "http://vxvault.net/ViriList.php/"


def sample_vxvault():
    try:
        soup = session.get(url)
        sample_dict = {}
        for i in soup.html.find("tr > td:nth-of-type(1) > a"):
            sample_link = "http://vxvault.net/" + i.attrs["href"]
            result = session.get(sample_link)
            sample_date = re.findall(r"<B>Added:</B> (.*?)<BR>", result.text)[0]
            if sample_date == download_date:
                sample_md5 = re.findall(r"<B>MD5:</B> (.*?)<BR>", result.text)[0]
                sample_url = f"http://" + re.findall(r"<B>Link:</B> hxxp://(.*?)<BR>", result.text)[0]
                sample_info = {
                    "sample_path": os.path.join(sample_all_dir, sample_md5 + ".vir"),
                    "sample_url": sample_url
                }
                sample_dict.update({sample_md5: sample_info})
            elif sample_date < download_date:
                break
    except Exception as e:
        return False, e
    else:
        if len(sample_dict) == 0:
            return False, "has`t data"
        else:
            return True, sample_dict
