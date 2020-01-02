#coding:utf-8
from bs4 import BeautifulSoup
import requests
from time import sleep
import json
from makejsonfile import Make_jsonfile,Send_area
from datetime import datetime as dt
import re

def Land_dict():
    dic = {}
    dic["ワールドバザール"] = ["オムニバス","ペニーアーケード"]
    dic["アドベンチャーランド"] = ["ウエスタンリバー鉄道","カリブの海賊","ジャングルクルーズ","ツリーハウス","魅惑のチキルーム"]
    dic["トゥーンタウン"] = ["ロジャーラビット","ミニーの家","ガジェットのゴーコースター","ドナルドのボート","トゥーンパーク"]
    dic["トゥモローランド"] = ["スティッチ・エンカウンター","スター・ツアーズ","スペース・マウンテン","モンスターズ・インク"]
    dic["ウエスタンランド"] = ["ビッグサンダー・マウンテン","シューティングギャラリー","カントリーベア・シアター","マークトウェイン号","トムソーヤ島いかだ"]
    dic["クリッターカントリー"] = ["スプラッシュ・マウンテン","カヌー探検"]
    dic["ファンタジーランド"] = ["ホーンテッド・マンション","プーさんのハニーハント","ピーターパン","白雪姫","シンデレラ","フィルハーマジック","ピノキオ","空飛ぶダンボ","キャッスルカルーセル","スモールワールド","アリスのティーパーティー"]

    return dic

def Check_park(date_words):
    #今の時間、日時を確認
    dt_now = dt.now()

    #今日の日付
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
        return "open"

    else:
        return "close"

def Scrape_day(soup):
    date = soup.find(class_ = "article_date")
    date = "2020年1月2日（木）"
    return date


def Set(park,area):

    #スクレイピングするサイトのURL
    if park == "land":
        #target_url = "https://www.google.com/"
        target_url = "https://disneyreal.asumirai.info/realtime/disneyland-wait-today.html"
        
    else:
        target_url = "https://disneyreal.asumirai.info/realtime/disneysea-wait-today.html"
    
    #アトラクションをエリア別に分けておく
    

    #サイトに負荷をかけないように待機する時間,URLにアクセス
    headers = {'User-Agent':'Mozilla/5.0'}
    html = requests.get(target_url,headers=headers)
    soup = BeautifulSoup(html.content,'lxml')

    result = soup.title.text
    print("ここかな")
    
    date_words = Scrape_day(soup)
    situation = Check_park(date_words)

    #閉園中
    if situation == "close":

        return "close"

    else:        
        return result

def main():
    print("これはpythonのみ開発モード")
    park = "land"
    area = "アドベンチャーランド"
    result = Set(park,area)
    print(result)


if __name__ == "__main__":
    main()
