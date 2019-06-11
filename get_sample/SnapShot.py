import os
import sys
import datetime
import requests
import warnings
warnings.filterwarnings("ignore")


class SnapShot:

	def __init__(self):
		date_download = self.get_date_download()
		session = self.get_session()
		self.start(session, date_download)

	@staticmethod
	def get_session():
		user = "iobit"
		pwd = "iobit#@6sample"
		session = requests.session()
		session.auth = (user, pwd)
		return session

	@staticmethod
	def get_date_download(days=1):
		date_today = datetime.datetime.today()
		date_interval = datetime.timedelta(days=days)
		date_download = date_today - date_interval
		return date_download.strftime("%Y%m%d")

	@staticmethod
	def download(download_url, session):
		base_dir = os.getcwd()
		file_name = download_url.split("/")[-1]
		file_path = os.path.join(base_dir, file_name)
		try:
			file_size = 0
			response = session.get(download_url, stream=True, verify=False)
			file_total_size = int(response.headers["content-length"])
			with open(file_path, "wb")as file:
				for chunk in response.iter_content(chunk_size=1024):
					if chunk:
						file.write(chunk)
						file_size += len(chunk)
						percent = int(file_size/file_total_size*100)
						print("\rdownload: ", "%s%%" % percent, end=" ")
			print("File download over")
		except requests.RequestException:
			print("404")

	@staticmethod
	def start(session, date_download):
		url_download_all = "https://www.snapshot.clamav.net/daily/snapshot-all-{}.zip.001".format(date_download)
		url_download_critical = "https://www.snapshot.clamav.net/daily/snapshot-critical-{}.zip.001".format(date_download)
		SnapShot.download(url_download_all, session)
		SnapShot.download(url_download_critical, session)


if __name__ == "__main__":
	SnapShot()
