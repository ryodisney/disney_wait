#coding:utf-8
from bs4 import BeautifulSoup
import requests
from time import sleep
import json
from makejsonfile import Make_jsonfile,Send_area
from datetime import datetime as dt
import re
import urllib3

def Land_dict(area):
    dic = {}
    dic["ワールドバザール"] = ["オムニバス"]
    dic["アドベンチャーランド"] = ["ウエスタンリバー鉄道","カリブの海賊","スイスファミリー・ツリーハウス","魅惑のチキルーム","ジャングルクルーズ：ワイルドライフ・エクスペディション"]
    dic["トゥーンタウン"] = ["ガジェットのゴーコースター","グーフィーのペイント＆プレイハウス","チップとデールのツリーハウス","トゥーンパーク","ドナルドのボート","ミッキーの家とミート・ミッキー","ミニーの家","ロジャーラビットのカートゥーンスピン"]
    dic["トゥモローランド"] = ["スターツアーズ","スペース・マウンテン","バズ・ライトイヤー","モンスターズ・インク","スティッチ・エンカウンター"]
    dic["ウエスタンランド"] = ["ウエスタンランド・シューティングギャラリー","カントリーベア・シアター","蒸気船マークトウェイン号","トムソーヤ島いかだ","ビッグサンダー・マウンテン","ウッドチャック・グリーティングトレイル（デイジー）","ウッドチャック・グリーティングトレイル（ドナルド）"]
    dic["クリッターカントリー"] = ["スプラッシュ・マウンテン","カヌー探検"]
    dic["ファンタジーランド"] = ["アリスのティーパーティー","イッツ・ア・スモールワールド","キャッスルカルーセル","白雪姫と七人の小人","シンデレラのフェアリーテイル･ホール","空飛ぶダンボ","ピノキオの冒険旅行","ピーターパン空の旅","プーさんのハニーハント","ホーンテッドマンション","ミッキーのフィルハーマジック"]

    attraction_area_extraction = dic[area]

    return attraction_area_extraction

def Check_park(business_hour):
    #今の時間、日時を確認
    dt_now = dt.now()

    #今日の日付
    year = int(dt_now.year)
    month = int(dt_now.month)
    day = int(dt_now.day)

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

#日にち取得
def Scrape_day(info_url):
    #開園時間取得
    html = requests.get(info_url,verify=False)
    soup = BeautifulSoup(html.content,'lxml')
    business_hour = soup.find(class_ = "business-hour").text
    business_hour_final = business_hour.strip()

    return business_hour

def Scrape_data(soup):
    attraction = []
    wait_time = []

    for attraction_temp in soup.find_all(class_ = "attr_name"):
        attraction.append(attraction_temp.text.strip())

    for wait_time_temp in soup.find_all(class_ = "attr_wait"):
        wait_time_treat = wait_time_temp.text.split("分")[0].strip()
        #中身が数字なら「分」を追加
        if wait_time_treat.isdecimal():
            wait_time_treat += "分"

        wait_time.append(wait_time_treat)
    
    return attraction,wait_time

def Wait_time_extraction(attraction_thisarea,attraction_all,wait_time_all):
    
    info_thisarea = []

    for attraction_goal in attraction_thisarea:

        for attraction,wait_time in zip(attraction_all,wait_time_all):
            if attraction_goal == attraction:
                if wait_time == "":
                    info_thisarea.append("情報がありません")
                else:
                    info_thisarea.append(wait_time)

    return info_thisarea

#ここでのmain関数
def Set(park,area):
    #警告を消すため
    urllib3.disable_warnings()

    #スクレイピングするサイトのURL
    if park == "land":
        #待ち時間のリンク
        target_url = "https://tokyodisneyresort.info/realtime.php?park=land&order=area_name"
        #開園時間や天気などのリンク
        info_url = "https://tokyodisneyresort.info/index.php?park=land"
        attraction_thisarea = Land_dict(area)

        
    else:
        target_url = "https://disneyreal.asumirai.info/realtime/disneysea-wait-today.html"
        dic = {}
    

    #開園時間をチェック
    business_hour = Scrape_day(info_url)
    #print(business_hour)
    situation = Check_park(business_hour)


    #閉園中
    if situation == "close":

        return "close"

    else:
        #headers = {'User-Agent':'Mozilla/5.0'}
        html = requests.get(target_url,verify=False)
        soup = BeautifulSoup(html.content,'lxml')

        attraction_all,wait_time_all = Scrape_data(soup)
        info_thisarea = Wait_time_extraction(attraction_thisarea,attraction_all,wait_time_all)
        #print(attraction_thisarea,info_thisarea)
        
        for attraction,info in zip(attraction_thisarea,info_thisarea):
            Send_area(area)
            Make_jsonfile(attraction,info)
    
        return "open"

def main():
    print("これはpythonのみ開発モード")
    park = "land"
    area = "アドベンチャーランド"
    result = Set(park,area)
    print(result)


if __name__ == "__main__":
    main()
