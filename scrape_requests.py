#coding:utf-8
from bs4 import BeautifulSoup
import requests
from time import sleep
import json
from makejsonfile import Make_jsonfile,Send_area,Reset_jsonfile
from datetime import datetime as dt
import re
import urllib3

#人気TOP10用リスト
def Land_pop_list():

    pop_list = ["オムニバス","ウエスタンリバー鉄道","カリブの海賊","ツリーハウス","魅惑のチキルーム","ジャングルクルーズ",\
        "ゴーコースター","プレイハウス","ツリーハウス","トゥーンパーク","ドナルドのボート","ミート・ミッキー","ミニーの家","カートゥーンスピン",\
        "スターツアーズ","スペース・マウンテン","バズ・ライトイヤー","モンスターズ・インク","スティッチ",\
        "シューティングギャラリー","カントリーベア","マークトウェイン号","トムソーヤ島いかだ","ビッグサンダー","トレイル（デイジー）","トレイル（ドナルド）",\
        "スプラッシュ","カヌー探検",\
        "ティーパーティー","スモールワールド","キャッスルカルーセル","白雪姫","フェアリーテイル","空飛ぶダンボ","ピノキオの冒険旅行","ピーターパン","ハニーハント","ホーンテッドマンション","フィルハーマジック"]

    return pop_list

#エリア別用リスト
def Land_area_dict(area):
    dic = {}
    dic["ワールドバザール"] = ["オムニバス"]
    dic["アドベンチャーランド"] = ["ウエスタンリバー鉄道","カリブの海賊","ツリーハウス","魅惑のチキルーム","ジャングルクルーズ"]
    dic["トゥーンタウン"] = ["ゴーコースター","プレイハウス","ツリーハウス","トゥーンパーク","ドナルドのボート","ミート・ミッキー","ミニーの家","カートゥーンスピン"]
    dic["トゥモローランド"] = ["スターツアーズ","スペース・マウンテン","バズ・ライトイヤー","モンスターズ・インク","スティッチ"]
    dic["ウエスタンランド"] = ["シューティングギャラリー","カントリーベア","マークトウェイン号","トムソーヤ島いかだ","ビッグサンダー","トレイル（デイジー）","トレイル（ドナルド）"]
    dic["クリッターカントリー"] = ["スプラッシュ","カヌー探検"]
    dic["ファンタジーランド"] = ["ティーパーティー","スモールワールド","キャッスルカルーセル","白雪姫","フェアリーテイル","空飛ぶダンボ","ピノキオの冒険旅行","ピーターパン","ハニーハント","ホーンテッドマンション","フィルハーマジック"]

    attraction_area_extraction = dic[area]

    return attraction_area_extraction

#人気TOP10用リスト
def Sea_pop_list():

    pop_list = ["ヴェネツィアン・ゴンドラ","エクスプロレーション","ディズニーシー･プラザ","スチーマーライン",\
                "タワー・オブ・テラー","タートル・トーク","トイ・ストーリー・マニア！","ビッグシティ・ヴィークル","グリーティングプレイス","スチーマーライン","レールウェイ","ウォーターフロントパーク","ケープコッド・クックオフ横",\
                "アクアトピア","レールウェイ","シーライダー",\
                "インディージョーンズ","スチーマーライン","レイジングスピリッツ","グリーティングドック","トレイル(グーフィー)","トレイル(ミニーマウス)","トレイル(ミッキーマウス)",\
                "キャラバンカルーセル","シンドバット","フライングカーペット","マジックランプシアター","アラビアンコースト",\
                "アリエルグリーティング","プレイグラウンド","ジェリーフィッシュ","スカットルのスクーター","フィッシュコースター","バルーンレース","ラグーンシアター","ワームプール",\
                "海底2万マイル","センター"]

    return pop_list

#エリア別用リスト
def Sea_area_dict(area):
    dic = {}
    dic["メディテレーニアンハーバー"] =["ヴェネツィアン・ゴンドラ","エクスプロレーション","ディズニーシー･プラザ","スチーマーライン"]
    dic["アメリカンウォーターフロント"] = ["タワー・オブ・テラー","タートル・トーク","トイ・ストーリー・マニア！","ビッグシティ・ヴィークル","グリーティングプレイス","スチーマーライン","レールウェイ","ウォーターフロントパーク","ケープコッド・クックオフ横"]
    dic["ポートディスカバリー"] = ["アクアトピア","レールウェイ","シーライダー"]
    dic["ロストリバーデルタ"] = ["インディージョーンズ","スチーマーライン","レイジングスピリッツ","グリーティングドック","トレイル(グーフィー)","トレイル(ミニーマウス)","トレイル(ミッキーマウス)"]
    dic["アラビアンコースト"] = ["キャラバンカルーセル","シンドバット","フライングカーペット","マジックランプシアター","アラビアンコースト"]
    dic["マーメイドラグーン"] = ["アリエルグリーティング","プレイグラウンド","ジェリーフィッシュ","スカットルのスクーター","フィッシュコースター","バルーンレース","ラグーンシアター","ワームプール"]
    dic["ミステリアスアイランド"] = ["海底2万マイル","センター"]

    attraction_area_extraction = dic[area]

    return attraction_area_extraction


#今が開園時間か確認
def Check_park(business_hour):
    #今の時間、日時を確認
    dt_now = dt.now()

    #今日の日付
    year = int(dt_now.year)
    month = int(dt_now.month)
    day = int(dt_now.day)

    #開園時間の分割
    open_time = business_hour.split("～")[0]
    if open_time.split(":")[0] == "":
        return "close"

    else:
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

#開園時間取得
def Scrape_day(info_url):
    html = requests.get(info_url,verify=False)
    soup = BeautifulSoup(html.content,'lxml')
    business_hour = soup.find(class_ = "business-hour").text
    business_hour_final = business_hour.strip()

    return business_hour_final

#待ち時間取得（エリア別）
def Scrape_data_area(soup):
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

#待ち時間取得（待ち時間TOP10）
def Scrape_data_top10(soup):
    attraction = []
    wait_time = []

    attraction_finded = soup.find_all(class_ = "attr_name")
    wait_time_finded = soup.find_all(class_ = "attr_wait")

    for counter,(attraction_temp,wait_time_temp) in enumerate(zip(attraction_finded,wait_time_finded)):
        if counter < 10:
            #temp2,3は\nと\tを削除するため
            wait_time_temp2 = wait_time_temp.text.split("分")[0].strip()
            wait_time_temp3 = wait_time_temp2.replace("\n","")
            wait_time_treat = wait_time_temp3.replace("\t","")
            
            #中身が数字なら「分」を追加
            if wait_time_treat.isdecimal():
                wait_time_treat += "分"
                #ここでappend
                attraction.append(attraction_temp.text.strip())
                wait_time.append(wait_time_treat)            
            counter += 1
        
        else:
            return attraction,wait_time
              
def Wait_time_extraction(attraction_thisarea,attraction_all,wait_time_all):
    
    info_thisarea = []

    for attraction_goal in attraction_thisarea:

        for attraction,wait_time in zip(attraction_all,wait_time_all):
            if attraction_goal in attraction:

                if "FP" in wait_time:
                    wait_time = wait_time.strip("【FP：TICKETING_END】") 

                if wait_time == "":
                    info_thisarea.append("情報なし")
                elif "案内終了" in wait_time:
                    info_thisarea.append("案内終了")
                else:
                    info_thisarea.append(wait_time)
                
    return info_thisarea

#表示のために名前を短くする関数
def Pop_shortname(attraction_pop_list,attraction_pop,wait_time_pop):

    attraction_pop_final = []
    info_pop = []

    for attraction_goal,wait_time in zip(attraction_pop,wait_time_pop):
        for attraction in attraction_pop_list:
            if attraction in attraction_goal:

                if "FP" in wait_time:
                    wait_time = wait_time.strip("【FP：TICKETING_END】") 

                info_pop.append(wait_time)
                attraction_pop_final.append(attraction)
    
    return attraction_pop_final,info_pop

def Scrare_data_show(soup):
    show = []
    wait_time = []

    for show_temp in soup.find_all(class_ = "attr_name"):
        show.append(show_temp.text.strip())

    for wait_time_temp in soup.find_all(class_ = "attr_wait"):
        wait_time_treat = wait_time_temp.text.strip()
        wait_time.append(wait_time_treat)

    return show,wait_time


#ここでのmain関数
def Set(park,area,info_url,target_url,genre):
    #警告を消すため
    urllib3.disable_warnings()

    #開園時間をチェック
    business_hour = Scrape_day(info_url)
    situation = Check_park(business_hour)

    #レシートのjsonファイルを初期化
    Reset_jsonfile()

    #閉園中
    if situation == "open":
        html = requests.get(target_url,verify=False)
        soup = BeautifulSoup(html.content,'lxml')

        #エリア別
        if genre == "エリア別":
            if park == "land":
                attraction_thisarea = Land_area_dict(area)
                
            elif park == "sea":
                attraction_thisarea = Sea_area_dict(area)

            attraction_all,wait_time_all = Scrape_data_area(soup)
            info_thisarea = Wait_time_extraction(attraction_thisarea,attraction_all,wait_time_all)
            #print(attraction_thisarea,info_thisarea)
            
            Send_area(area)

            for attraction,info in zip(attraction_thisarea,info_thisarea):
                Make_jsonfile(attraction,info)

        elif genre == "待ち時間TOP10":

            if park == "land":
                attraction_pop_list = Land_pop_list()
                
            elif park == "sea":
                attraction_pop_list = Sea_pop_list()

            attraction_pop,wait_time_pop = Scrape_data_top10(soup)
            print(attraction_pop)
            attraction_pop_final,info_pop = Pop_shortname(attraction_pop_list,attraction_pop,wait_time_pop)
            print(attraction_pop_final)
            
            Send_area("待ち時間TOP10")

            for attraction,info in zip(attraction_pop_final,info_pop):
                Make_jsonfile(attraction,info)
            
        return "open"
    
    #閉園中
    else:    
        return "close"

def main():
    print("これはpythonのみ開発モード")
    park = "sea"
    area = "ロストリバーデルタ"
    #開園時間や天気などのリンク
    info_url = "https://tokyodisneyresort.info/index.php?park=sea"
    target_url = "https://tokyodisneyresort.info/realtime.php?park=sea&order=wait"
    genre = "待ち時間TOP10"

    result = Set(park,area,info_url,target_url,genre)
    print(result)


if __name__ == "__main__":
    main()
