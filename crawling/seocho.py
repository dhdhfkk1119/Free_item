from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
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
urls = [
    "https://www.scscc.or.kr/toy/toy/toy_list.asp?SC_SEQ_SEQ=2",
    "https://www.scscc.or.kr/toy/toy/toy_list.asp?SC_SEQ_SEQ=3",
    "https://www.scscc.or.kr/toy/toy/toy_list.asp?SC_SEQ_SEQ=4",
    "https://www.scscc.or.kr/toy/toy/toy_list.asp?SC_SEQ_SEQ=5",
    "https://www.scscc.or.kr/toy/toy/toy_list.asp?SC_SEQ_SEQ=6"
]

try:
    for url in urls:
        # 페이지 이동
        driver.get(url)
        while True:
            # 현재 페이지의 HTML을 BeautifulSoup을 사용하여 파싱
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # 반복하는 리스트 정보 가져오기
            product = soup.select(".card-list > ul > li")

            for p in product:
                # 이름 가져오기
                name_tag = p.select_one("p.title")
                name = name_tag.text.strip() if name_tag else "Name not found"

                # 나이 정보 가져오기
                age_tag = p.select_one("span.small-txt")
                age = age_tag.text.strip() if age_tag else "Age not found"

                # 대여 상태 가져오기
                status_tag_line = p.select_one("strong.card-btn.line")
                status_tag_available = p.select_one("strong.card-btn")

                status_tag = status_tag_line if status_tag_line else status_tag_available
                status = status_tag.text.strip() if status_tag else "Status not found"

                # 이미지 주소 가져오기
                img_tag = p.select_one("span.img-box > img")
                img_src = img_tag.get("src") if img_tag else "Image not found"
                full_img_src = img_src
                detail_url = driver.current_url

                insert_item(conn,name, age, status, full_img_src,detail_url)

                print("상세 주소:", detail_url)
                print("이미지 주소:", img_src)
                print("이름:", name)
                print("나이:", age)
                print("대여상태:", status)
                print("-------------------------------")

            try:
                # 현재 페이지의 HTML을 가져와서 BeautifulSoup 객체를 업데이트
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # 마지막 페이지 확인
                last_page_check = soup.select_one(".num.active")
                if not last_page_check.find_next_sibling(class_="num"):
                    print("마지막 페이지에 도달했습니다.")
                    break

                # 다음 페이지로 이동
                next_page_link = driver.find_element(By.CSS_SELECTOR, "a.page.next")
                next_page_link.click()

            except NoSuchElementException:
                # 다음 페이지 링크가 없을 때
                print("마지막 페이지에 도달했습니다.")
                break
finally:
    # WebDriver 종료
    driver.quit()
    conn.close()