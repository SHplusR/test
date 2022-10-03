import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


import warnings
warnings.filterwarnings("ignore")

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time

# brew 로 설치된 chromedriver의 path (Mac)
path = '/Users/hyorisim/Downloads/chromedriver'

# 크롤링할 사이트 주소를 정의합니다.
source_url = "https://map.kakao.com/"

# 크롬 드라이버를 사용합니다
driver = webdriver.Chrome(path)

# 카카오 지도에 접속합니다
driver.get(source_url)

# 검색창에 검색어를 입력합니다

searchbox = driver.find_element(By.XPATH,"//input[@id='search.keyword.query']")

searchbox.send_keys("카페")

# 검색버튼을 눌러서 결과를 가져옵니다

searchbutton = driver.find_element(By.XPATH,"//button[@id='search.keyword.submit']")
driver.execute_script("arguments[0].click();", searchbutton)

# 검색 결과를 가져올 시간을 기다립니다
time.sleep(2)

# 장소 더보기
moreplace = driver.find_element(By.ID,"info.search.place.more")
driver.execute_script("arguments[0].click();", moreplace)

page_urls = []

for button_num in range(1,6) :
    another_reviews = driver.find_element(By.XPATH," //*[@id='info.search.page.no" + str(button_num) + "']")
    another_reviews.click()
    html = driver.page_source

    # BeautifulSoup을 이용하여 html 정보를 파싱
    soup = BeautifulSoup(html, "html.parser")
    moreviews = soup.find_all(name="a", attrs={"class": "moreview"})

    for moreview in moreviews:
        page_url = moreview.get("href")
        page_urls.append(page_url)
        print(page_urls)

# 장소 더보기 클릭합니다.
# 1페이지로 이동합니다.
# 2페이지로 이동합니다.
# 5페이지 이상은 다음 버튼으로 넘어갑니다.


# a태그의 href 속성을 리스트로 추출하여, 크롤링 할 페이지 리스트를 생성



# 크롤링에 사용한 브라우저를 종료합니다.
driver.close()

columns = ['score', 'review']
df = pd.DataFrame(columns=columns)

driver = webdriver.Chrome(path)  # for Mac

for page_url in page_urls:
    driver.get(page_url)
    time.sleep(2)

    # 첫 페이지 리뷰를 크롤링합니다
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    contents_div = soup.find(name="ul", attrs={"class": "list_evaluation"})

    if contents_div :
        rates = contents_div.find_all(name="span", attrs={"class": "ico_star star_rate"})
        reviews = contents_div.find_all(name="p", attrs={"class": "txt_comment"})

        for rate, review in zip(rates, reviews):
            row = [rate.find('span', 'ico_star inner_star')['style'][-5:-2], review.find(name="span").text]
            print(row)
            series = pd.Series(row, index=df.columns)
            df = df.append(series, ignore_index=True)

    else:
        continue

    print("for is over")


driver.close()



print("excel start")

df.to_excel("review_data.xlsx", index=False)
print("done")