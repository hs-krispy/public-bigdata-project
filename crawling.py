from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import re

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# 네이버 지도
browser = webdriver.Chrome("C:/python/chromedriver.exe", options=options)
url = "https://map.naver.com/v5/?c=14153475.8171924,4477924.1397080,15,0,0,0,dh"
browser.get(url)
time.sleep(5)
gu = ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구",
      "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"]

df_list = []
for g in gu:
    print(g + " 배달대행")
    # text box clear
    browser.find_element_by_xpath(
        '/html/body/app/layout/div[3]/div[2]/shrinkable-layout/div/app-base/search-input-box/div/div[1]/div/input').clear()
    time.sleep(1)
    # input
    browser.find_element_by_xpath(
        '/html/body/app/layout/div[3]/div[2]/shrinkable-layout/div/app-base/search-input-box/div/div[1]/div/input').send_keys(
        g + " 배달대행")
    time.sleep(1)
    browser.find_element_by_xpath(
        '/html/body/app/layout/div[3]/div[2]/shrinkable-layout/div/app-base/search-input-box/div/div[1]/div/input').send_keys(
        Keys.ENTER)
    time.sleep(1)
    # iframe으로 browser 전환
    browser.switch_to.frame('searchIframe')
    i = 0
    while True:
        i += 1
        try:
            li = browser.find_element_by_xpath(f'//*[@id="_pcmap_list_scroll_container"]/ul/li[{i}]')
            time.sleep(2)
        except:
            last_page = browser.find_elements_by_css_selector('#app-root > div > div > div._2ky45 > a._2tk2s')[-1].text
            time.sleep(2)
            current_page = browser.find_element_by_css_selector(
                '#app-root > div > div > div._2ky45 > a._2tk2s._3F99o').text
            time.sleep(2)
            print(current_page, last_page)
            # 모든 page 순회
            if current_page < last_page:
                print("click next page")
                browser.find_element_by_xpath('//*[@id="app-root"]/div/div/div[2]/a[5]').send_keys(Keys.ENTER)
                i = 1
            # 마지막 page 이후
            else:
                browser.switch_to.default_content()
                time.sleep(3)
                break
        time.sleep(2)
        li = browser.find_element_by_xpath(f'//*[@id="_pcmap_list_scroll_container"]/ul/li[{i}]')
        time.sleep(1)
        # 각 구에 해당하는 결과만 filtering
        match = re.search("서울 " + g, li.find_element_by_class_name('_1AEUt').text)
        if match is None:
            continue
        li.find_element_by_class_name('_1AEUt').send_keys(Keys.ENTER)
        time.sleep(1)
        df = pd.DataFrame({
            "상호명": [li.find_element_by_class_name('_3Apve').text],
            "도로명 주소": [re.sub("도로명|\n복사", "", li.find_element_by_class_name('_2b9ic').text)]
        })
        print(i)
        print(df)
        df_list.append(df)

seoul = pd.concat(df_list)
seoul.to_csv("서울시 배달대행 주소.csv", index=False)
