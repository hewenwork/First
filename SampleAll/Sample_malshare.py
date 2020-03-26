from First.SampleAll.InitFile import *


def sample_malshare():
    url = f"https://malshare.com/api.php"
    option = {
        "params": {
            "api_key": "2befc1c0b4d476b8527887f3f415648050638eff8dd400071f694e7356d5e49a",
            "action": "getlist"
        },
        "auth": ("infected", "infected")
    }
    try:
        sample_dict = {}
        response = session.get(url, **option).json()
        option["params"].update({"action": "getfile"})
        for sample in response:
            sample_md5 = sample["md5"]
            sample_name = sample_md5 + ".vir"
            sample_url = "https://malshare.com/api.php"
            option["params"].update({"hash": sample_md5})
            sample_info = {
                "sample_path": os.path.join(sample_all_dir, sample_name),
                "sample_url": sample_url,
                "option": option
            }
            sample_dict.update({sample_md5: sample_info})
        return True, sample_dict
    except Exception as e:
        return False, e


if __name__ == "__main__":
    result = sample_malshare()
    print(result)
