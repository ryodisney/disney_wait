#coding:utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import json
from makejsonfile import Make_jsonfile,Send_area

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

def Close(html):
    close_flag = False
    soup = BeautifulSoup(html,"lxml")
    print("サイトのタイトル = " + str(soup.title.text))

    close_tag = soup.find_all('div',class_ = "close")

    if close_tag is not None:
        close_flag = True
    
    return close_flag

def Set(park,area):
    options = Options()
    options.set_headless(True)
    options.add_argument('--headless')
    #driver_path = "C:/Users/ryo/Desktop/chromedriver_win32/chromedriver.exe"
    options.add_argument("--user-agent=Mozilla/5.0")
    driver = webdriver.Chrome(options=options)

    #スクレイピングするサイトのURL
    if park == "land":
        target_url = "https://www.tokyodisneyresort.jp/tdl/realtime/attraction/"
    else:
        target_url = "https://www.tokyodisneyresort.jp/tds/realtime/attraction/"
    
    #サイトに負荷をかけないように待機する時間,URLにアクセス
    INTERVAL = 1
    driver.get(target_url)
    html = driver.page_source

    close_flag = Close(html)
    print(close_flag)
    #閉園中
    if close_flag == "True":
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
