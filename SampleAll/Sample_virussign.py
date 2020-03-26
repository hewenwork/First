from First.SampleAll.InitFile import *


def sample_virusign():
    url = f"http://www.virusign.com/get_hashlist.php"
    params = {
        "md5": "",
        "sha256": "",
        "start_date": download_date,
        "end_date": download_date
    }
    auth = ("infected", "infected")
    try:
        sample_dict = {}
        response = session.get(url, params=params, timeout=40).text
        sha256_list = re.findall(r"\"(\w{64})\"", response)
        md5_list = re.findall(r"\"\w{64}\",\"(\w{32})\"", response)
        for sample_md5, sample_sah256 in zip(md5_list, sha256_list):
            sample_info = {
                "sample_path": os.path.join(sample_all_dir, sample_md5 + ".7z"),
                "sample_url": f"http://virusign.com/file/{sample_sah256}.7z",
                "auth": auth
            }
            sample_dict.update({sample_md5: sample_info})
        if len(sample_dict) == 0:
            information = f"website today num is 0."
            return False, information
        else:
            return True, sample_dict
    except Exception as e:
        information = f"parse website error {e}."
        return False, information


if __name__ == "__main__":
    a = sample_virusign()
    print(a)