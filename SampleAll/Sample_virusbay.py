from First.SampleAll.InitFile import *


def sample_virusbay():
    login_url = "https://beta.virusbay.io/login"
    data = {
        "email": "niwangxiu@gmail.com",
        "password": "testvirus0504L"
    }
    sample_dict = {}
    try:
        response = session.post(url=login_url, data=data)
        token = response.json()["token"]
        authorization = {"Authorization": "JWT %s" % token}
        session.headers.update(authorization)
        data_url = "https://beta.virusbay.io/sample/data"
        recent = session.get(url=data_url).json()["recent"]
        for sample in recent:
            sample_date = sample["publishDate"][:10]
            if download_date == sample_date:
                sample_md5 = sample["md5"]
                sample_name = sample_md5 + ".vir"
                sample_link = "https://beta.virusbay.io/api/sample/%s/download/link" % sample["_id"]
                sample_url = session.get(sample_link).text
                sample_info = {
                    "sample_path": os.path.join(sample_dir, sample_name),
                    "sample_url": sample_url
                }
                sample_dict.update({sample_md5: sample_info})
        return True, sample_dict
    except Exception as e:
        return False, e


if __name__ == "__main__":
    result = sample_virusbay()
    print(result)
