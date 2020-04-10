import os
from datetime import datetime, timedelta

download_dir = r"G:\LimitedFree"

if os.path.exists(download_dir) is False:
    os.makedirs(download_dir)


def sample_limitedfree(download_date):
    if isinstance(download_date, datetime) is False:
        return False, f"{download_date} is not isinstance datetime"
    sample_date = download_date.strftime("%Y%m%d")
    sample_name = f"virussign.com_{sample_date}_LimitedFree.zip"
    sample_url = f"http://samples.virussign.com/samples/{sample_name}"
    sample_info = {
        "sample_path": os.path.join(download_dir, sample_name),
        "sample_name": sample_name,
        "sample_url": sample_url,
        "auth": ("f_yunwing1", "9kkSkk3dSd"),
        "stream": True,
        "is_archive": True
    }
    return True, [sample_info]


if __name__ == "__main__":
    a = sample_limitedfree(datetime.today())
    print(a)
