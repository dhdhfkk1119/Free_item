from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse

# Selenium을 사용하여 웹 드라이버 시작
driver = webdriver.Chrome()  # 또는 사용하는 브라우저에 맞게 다른 드라이버를 선택

# 첫 번째 페이지의 URL
url = "https://www.toyplaza.or.kr/main/main.php?categoryid=03&menuid=01&groupid=00"

# 페이지 이동
driver.get(url)

try:
    while True:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.pd_item"))  # 확인할 요소 지정
        )

        # 현재 페이지의 HTML을 가져와서 BeautifulSoup 객체를 업데이트
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 반복하는 리스트 정보 가져오기
        product = soup.select("li.pd_item")

        for p in product:
            # 이름 가져오기
            name_tag = p.select_one("span.toy_name")
            name = name_tag.text.strip() if name_tag else "Name not found"

            # 나이 정보 가져오기
            age_tag = p.select_one("span.use_year")
            age = age_tag.text.strip() if age_tag else "Free"

            # 대여 상태 가져오기
            status = "대여 정보 없음"

            # 이미지 주소 가져오기
            img_tag = p.select_one("li.pd_item > a > img")
            img_src = img_tag.get("src") if img_tag else "Image not found"
            full_img_src = urllib.parse.urljoin("https://www.toyplaza.or.kr", img_src)

            print("이미지 주소:", full_img_src)
            print("이름:", name)
            print("나이:", age)
            print("대여상태:", status)
            print("-------------------------------")

        # 다음 페이지 링크를 찾고 클릭
        try:
            next_page_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.select + span a'))
            )
            next_page_button.click()
        except TimeoutException:
            print("마지막 페이지에 도달했습니다.")
            break
finally:
    driver.quit()
