from First.SampleAll.InitFile import *


def sample():
    file_name = f"[infected]UrlHash{download_date}.zip"
    file_path = os.path.join(sample_urlhaus_dir, file_name)
    download_url = f"https://urlhaus-api.abuse.ch/downloads/{download_date}.zip"
    return {
        "sample_path": file_path,
        "sample_url": download_url
    }


