from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
import pymysql
from insert_item import insert_item  # insert_item 함수를 임포트
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    db='toy',
    charset='utf8'
)


# Selenium을 사용하여 웹 드라이버 시작
driver = webdriver.Chrome()  # 또는 사용하는 브라우저에 맞게 다른 드라이버를 선택

# 첫 번째 페이지의 URL
url = "https://www.gskids.or.kr/gsplay/toy/toy-list"

# 페이지 이동
driver.get(url)

try:
    while True:
        # 현재 페이지의 HTML을 BeautifulSoup을 사용하여 파싱
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 반복하는 리스트 정보 가져오기
        product = soup.select(".tb-col > tbody > tr")

        for p in product:
            # 이름 가져오기
            name_tag = p.select_one("td.__left")
            name = name_tag.text.strip() if name_tag else "Name not found"

            # 나이 정보 가져오기
            age_tag = p.select_one("td:contains('이상')")
            age = age_tag.text.strip() if age_tag else "Age not found"

            # 대여 상태 태그 가져오기
            status_tag_line = p.select_one(".entry-tag.tag01")
            if status_tag_line:
                # 텍스트로부터 '1개' 값을 가져옴
                status_text = status_tag_line.next_sibling.strip()
                # '1'이 포함되어 있는지 확인
                if '1' in status_text:
                    status = "대여가능"
                else:
                    status = "예약중"

            # 이미지 주소 가져오기
            img_tag = p.select_one(".tb-col > tbody > tr > td > img")            
            img_src = img_tag.get("src") if img_tag else "Image not found"
            img_url = "https://www.gskids.or.kr"
            full_img_src = urljoin(img_url, img_src)
            detail_url = driver.current_url

            insert_item(conn,name,age,status,full_img_src,detail_url)

            print("이미지 주소:", full_img_src)
            print("이름:", name)
            print("나이:", age)
            print("대여상태:", status)
            print("-------------------------------")

    
        try:
            # 현재 페이지의 HTML을 가져와서 BeautifulSoup 객체를 업데이트
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # 다음 페이지로 이동
            next_page_link = driver.find_element(By.CSS_SELECTOR, "a.nextpostslink")
            next_page_link.click()

        except NoSuchElementException:
            # 다음 페이지 링크가 없을 때
            print("마지막 페이지에 도달했습니다.")
            break
        
finally:
    # WebDriver 종료
    driver.quit()
    conn.close()


