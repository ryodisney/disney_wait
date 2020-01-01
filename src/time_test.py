#cording:utf-8
from datetime import datetime as dt
import re

#今の時間、日時を確認
dt_now = dt.now()
dt_date = dt_now.date()

#今日の日付
date_words = "2020年1月2日（木）"
date_info = re.sub("\\D","-",date_words)
date_split = date_info.split("-",3)
year = int(date_split[0])
month = int(date_split[1])
day = int(date_split[2])

#今日の営業時間
business_hour = "8:00 ～ 22:00"

#開園時間の分割
open_time = business_hour.split("～")[0]
open_hour = int(open_time.split(":")[0])
open_minute = int(open_time.split(":")[1])

#閉園時間の分割
close_time = business_hour.split("～")[1]
close_hour = int(close_time.split(":")[0])
close_minute = int(close_time.split(":")[1])

#datetime化
open_datetime = dt(year,month,day,open_hour,open_minute)
close_datetime = dt(year,month,day,close_hour,close_minute)

if open_datetime < dt_now < close_datetime:
    print("運営中")
else:
    print("閉園中")

