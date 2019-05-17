import datetime
import os
import shutil

user_desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
date_today = datetime.datetime.today()
date_yestoday = date_today - datetime.timedelta(days=1)
old_path = os.path.join(user_desktop_path, "OLD")
yestoday_path = os.path.join(user_desktop_path, date_yestoday.strftime("%Y%m%d"))
today_path = os.path.join(user_desktop_path, date_today.strftime("%Y%m%d"))
if os.path.exists(yestoday_path):
    shutil.move(yestoday_path, old_path)
os.makedirs(today_path)
