#coding:utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import json
from makejsonfile import Make_jsonfile,Send_area
from datetime import datetime as dt
import re

def Scrape(html):
    attraction_list = []
    info_list = []
    soup = BeautifulSoup(html,"lxml")
    
    for search_tag in soup.find_all(class_ = 'areaName'):
        area_name = search_tag.text.strip()
        #アトラクションの名前と運転状況
        attraction_info = search_tag.parent
        attraction_name = attraction_info.find('h3').text.strip()
        attraction_list.append(attraction_name)
        current_info_temp = attraction_info.find(class_ = "operation")
        if current_info_temp is None:
            current_info = "運営中止"
        else:
            current_info = current_info_temp.text.strip()
        #print(attraction_name,current_info)

        if current_info == "運営中":
            wait_status = attraction_info.find(class_ = "waitingTime").text.strip()
            if "分" in wait_status:
                wait_time = str(attraction_info.find(class_ = "time").text.strip()) + "分"
            else:
                wait_time = wait_status
                
            update_time = attraction_info.find(class_ = "update").text.strip()
            info_list.append([area_name,wait_time,update_time])
        
        else:
            update_time = attraction_info.find(class_ = "update").text.strip()
            info_list.append([area_name,current_info,update_time])
    
    return attraction_list,info_list

def Match_area(attraction_list,info_list,area):
    attraction_thisarea = []
    info_thisarea = []
    for attraction_name,attraction_info in zip(attraction_list,info_list):
        if attraction_info[0] == area:
            del attraction_info[0]
            attraction_thisarea.append(attraction_name)
            info_thisarea.append(attraction_info)
    

    return attraction_thisarea,info_thisarea



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

def Scrape_day(html):
    soup = BeautifulSoup(html,"lxml")
    print(soup.title.text)
    print("ここかな")
    date = soup.find(class_ = "article_date")
    date = "2020年1月2日（木）"
    return date


def Set(park,area):
    options = webdriver.ChromeOptions()
    options.set_headless(True)
    options.add_argument('--headless')
    options.add_argument('--user-agent=Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)')
    driver = webdriver.Chrome(options=options)

    #スクレイピングするサイトのURL
    if park == "land":
        target_url = "https://disneyreal.asumirai.info/realtime/disneyland-wait-today.html"
        
    else:
        target_url = "https://disneyreal.asumirai.info/realtime/disneysea-wait-today.html"
    
    #アトラクションをエリア別に分けておく
    

    #サイトに負荷をかけないように待機する時間,URLにアクセス
    INTERVAL = 1
    driver.get(target_url)
    html = driver.page_source

    date_words = Scrape_day(html)
    situation = Check_park(date_words)

    #閉園中
    if situation == "close":
        sleep(INTERVAL)
        driver.quit()
        return "close"

    else:
        attraction_list,info_list = Scrape(html)
        attraction_thisarea,info_thisarea = Match_area(attraction_list,info_list,area)
        Send_area(area)
        print(attraction_thisarea,info_thisarea)
        for attraction,info in zip(attraction_thisarea,info_thisarea):
            Make_jsonfile(attraction,info)
        
        sleep(INTERVAL)
        driver.quit()
        
        return "open"

def main():
    print("これはpythonのみ開発モード")
    park = "land"
    area = "アドベンチャーランド"
    Set(park,area)


if __name__ == "__main__":
    main()
