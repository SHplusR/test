import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re
import time

# brew 로 설치된 chromedriver의 path (Mac)
path = '/Users/hyorisim/Downloads/chromedriver'

# 크롤링할 사이트 주소를 정의합니다.
source_url = "https://map.kakao.com/"

# 크롬 드라이버를 사용합니다 (맥은 첫 줄, 윈도우는 두번째 줄 실행)
driver = webdriver.Chrome(path)

# 카카오 지도에 접속합니다
driver.get(source_url)

# 검색창에 검색어를 입력합니다

searchbox = driver.find_element(By.XPATH,"//input[@id='search.keyword.query']")

searchbox.send_keys("강남역 고기집")

# 검색버튼을 눌러서 결과를 가져옵니다

searchbutton = driver.find_element(By.XPATH,"//button[@id='search.keyword.submit']")
driver.execute_script("arguments[0].click();", searchbutton)

# 검색 결과를 가져올 시간을 기다립니다
time.sleep(2)

# 검색 결과의 페이지 소스를 가져옵니다
html = driver.page_source

# BeautifulSoup을 이용하여 html 정보를 파싱합니다
soup = BeautifulSoup(html, "html.parser")
moreviews = soup.find_all(name="a", attrs={"class":"moreview"})

# a태그의 href 속성을 리스트로 추출하여, 크롤링 할 페이지 리스트를 생성합니다.
page_urls = []
for moreview in moreviews:
    page_url = moreview.get("href")
    print(page_url)
    page_urls.append(page_url)

# 크롤링에 사용한 브라우저를 종료합니다.
driver.close()

columns = ['score', 'review']
df = pd.DataFrame(columns=columns)

driver = webdriver.Chrome(path)  # for Mac




for page_url in page_urls:

    # 상세보기 페이지에 접속합니다
    driver.get(page_url)
    time.sleep(2)

    # 첫 페이지 리뷰를 크롤링합니다
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    contents_div = soup.find(name="ul", attrs={"class": "list_evaluation"})
    print(contents_div)
    # 별점을 가져옵니다.
    rates = contents_div.find_all(name="div", attrs={"class": "ico_star star_rate"})
    #rates = contents_div.find_all(name="p", attrs={"class": "txt_comment"})
    print("rates  ================== ",rates)


    # 리뷰를 가져옵니다.
    reviews = contents_div.find_all(name="p", attrs={"class": "txt_comment"})
    print("reviews  ================== ",reviews)

    for rate, review in zip(rates, reviews):
        print("rate is",rate)
        print("raree is", reviews)
        for stars in rate:
            stars = {}
            print('rate.select : ',rate.select('div > div'))
            stars['style'] = rate.select('div > div')
            print("in loop review is", review.find(name="span").text)
            row = [stars['style'], review.find(name="span").text]
            series = pd.Series(row, index=df.columns)
            df = df.append(series, ignore_index=True)

    print("for is over")

    # 2-5페이지의 리뷰를 크롤링합니다
    # for button_num in range(2, 6):
    #     print("2-5 for start")
    #     # 오류가 나는 경우(리뷰 페이지가 없는 경우), 수행하지 않습니다.
    #     try:
    #         another_reviews = driver.find_element_by_xpath("//a[@data-page='" + str(button_num) + "']")
    #         another_reviews.click()
    #         time.sleep(2)
    #
    #         # 페이지 리뷰를 크롤링합니다
    #         html = driver.page_source
    #         soup = BeautifulSoup(html, 'html.parser')
    #         contents_div = soup.find(name="div", attrs={"class": "evaluation_review"})
    #
    #         # 별점을 가져옵니다.
    #         rates = contents_div.find_all(name="span", attrs={"class": "ico_star inner_star"})
    #
    #         # 리뷰를 가져옵니다.
    #         reviews = contents_div.find_all(name="p", attrs={"class": "txt_comment"})
    #
    #         for rate, review in zip(rates, reviews):
    #
    #             row = [rate["style"], review.find(name="span").text]
    #             series = pd.Series(row, index=df.columns)
    #             df = df.append(series, ignore_index=True)
    #     except:
    #         break



driver.close()



print("excel start")
df['y'] = df['score'].apply(lambda x: 1 if float(x) > 3 else 0)
print(df.shape)

df.to_excel("review_data.xlsx", index=False)
print("done")