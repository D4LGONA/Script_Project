from selenium.webdriver.common.by import By
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
from selenium.webdriver.common.keys import Keys
import time
import requests

#크롬 웹드라이버 불러오기
driver = webdriver.Chrome(ChromeDriverManager().install())
res = driver.get('https://m.place.naver.com/place/list?query=%EA%B0%95%EB%82%A8%EA%B5%AC%20%EC%B9%B4%ED%8E%98&level=top')
driver.implicitly_wait(20)

#2차 크롤링을 위한 bs4 셋팅
session = requests.Session()
headers = {"User-Agent": "useragent값 넣어주기"}

retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])

session.mount('http://', HTTPAdapter(max_retries=retries))

#body부분을 잡기 위해 쓸데없이 버튼을 클릭해줌
driver.find_element(By.XPATH, '//*[@id="_list_scroll_container"]/div/div/div[1]/div/div/a[2]').click()
driver.find_element(By.XPATH, '//*[@id="_list_scroll_container"]/div/div/div[1]/div/div/a[1]').click()

#검색결과가 모두 보이지 않기 때문에 page down을 눌러 끝까지 펼쳐준다.
for scroll in range(0,30):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)

html = driver.page_source
bs = BeautifulSoup(html, 'html.parser')
soup = bs.select_one('div.YluNG')
naver_info = soup.select('li.VLTHu')

#2차 크롤링을 위한 url
url = 'https://m.place.naver.com'

for info in naver_info:

    store_name = info.select_one('div.C6RjW').text
    mart_cate = info.select_one('span.YzBgS').text
    link = info.select_one('div.ouxiq').select_one('a').attrs['href']
    time.sleep(0.06)

    #네이버 플레이스로 이동(place ID로 접속)
    N_res = session.get(url+link, headers=headers)
    N_soup_srch = BeautifulSoup(N_res.content, 'html.parser')
    mart_oldtel = N_soup_srch.select_one('span.yxkiA > a').attrs['href']
    mart_tel = str(re.sub('tel:', '', mart_oldtel)) # 'tel:' 삭제

    #주소는 '공유'에서 파싱
    address = N_soup_srch.select('span.yxkiA > a')[3].attrs['data-line-description']

    print(store_name, '/',store_cate, '/', url+link, '/',  store_tel, '/', address )
    time.sleep(0.06)
