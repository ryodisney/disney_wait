#coding:utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

def Scrape():
    options = Options()
    options.set_headless(True)
    driver_path = "C:/Users/ryo/Desktop/必要なモノ/chromedriver_win32/chromedriver"
    driver = webdriver.Chrome(driver_path,options=options)

    #スクレイピングするサイトのURL
    target_url = "http://www15.plala.or.jp/gcap/disney/realtime.htm"
    
    #サイトに負荷をかけないように待機する時間,URLにアクセス
    INTERVAL = 3
    driver.get(target_url)

def main():
    print("これが出力されることはない")


if __name__ == "__main__":
    main()
