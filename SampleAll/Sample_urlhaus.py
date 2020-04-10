import os
from datetime import datetime, timedelta


def sample_urlhaus(download_date):
    sample_dir = r"G:\Urlhaus"
    sample_date = download_date.strftime("%Y-%m-%d")
    sample_name = f"[infected]_UrlHash_{sample_date}.zip"
    download_url = f"https://urlhaus-api.abuse.ch/downloads/{sample_date}.zip"
    sample_info = {
        "sample_path": os.path.join(sample_dir, sample_name),
        "sample_url": download_url,
        "stream": True,
        "is_archive": True
    }
    return True, [sample_info]


if __name__ == "__main__":
    print(sample_urlhaus(datetime.today() - timedelta(days=3)))
