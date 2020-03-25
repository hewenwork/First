from First.SampleAll.InitFile import *


def sample_traffic():
    sample_dict = {}
    sample_date = download_date.replace("-", "/")
    url = f"http://www.malware-traffic-analysis.net/{sample_date}/"
    try:
        result = session.get(url + "index.html")
        soup = result.html.find("ul > li > a") if result.status_code == 200 else None
        if soup is None:
            return False, "has`t data"
        for line in soup:
            sample_name = line.attrs["href"]
            if "-malware" in sample_name:
                sample_url = url + sample_name
                sample_info = {
                    "sample_path": os.path.join(sample_dir, sample_name),
                    "sample_url": sample_url
                }
                sample_dict.update({sample_name: sample_info})
        return True, sample_dict
    except Exception as e:
        return False, e


if __name__ == "__main__":
    print(sample_traffic())
