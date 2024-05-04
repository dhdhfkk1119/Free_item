from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import insert_item
# DB 연결 가져오기
conn = insert_item.get_db_connection()

# Selenium을 사용하여 웹 드라이버 시작
driver = webdriver.Chrome()  # 또는 사용하는 브라우저에 맞게 다른 드라이버를 선택

# 다중페이지 URL
urls = [
    "https://www.gncare.go.kr/main/main.php?categoryid=44&menuid=02&groupid=00",
    "https://www.gncare.go.kr/main/main.php?categoryid=43&menuid=02&groupid=00",
    "https://www.gncare.go.kr/main/main.php?categoryid=45&menuid=02&groupid=00",
    "https://www.gncare.go.kr/main/main.php?categoryid=48&menuid=02&groupid=00"
]

try:
    for url in urls:
        # 페이지 이동
        driver.get(url)
        while True:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "dl.toySR_list"))  # 확인할 요소 지정
            )

            # 현재 페이지의 HTML을 가져와서 BeautifulSoup 객체를 업데이트
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # 반복하는 리스트 정보 가져오기
            product = soup.select("dl.toySR_list")

            for p in product:
                # 이름 가져오기
                name_tag = p.select_one("span.toy_name")
                name = name_tag.text.strip() if name_tag else "Name not found"

                # 나이 정보 가져오기
                age = "전체연령"

                # 대여 상태 가져오기
                table = p.find_next("table", class_="marT05")
                if table:
                    # 대여 가능 여부를 확인하는 셀(td) 요소를 가져옴
                    available_cell = table.find("th", class_="t_state01")
                    # 대여 가능 여부 확인
                    next_sibling_td = available_cell.find_next_sibling("td")
                    available = next_sibling_td.get_text().strip() if next_sibling_td else ""
                    status = "대여가능" if available != "0" else "예약중"
                else:
                    status = "예약중"

                # 이미지 주소 가져오기
                img_tag = p.select_one("dl.toySR_list > dt > img")
                img_src = img_tag.get("src") if img_tag else "Image not found"
                full_img_src = urllib.parse.urljoin("https://www.gncare.go.kr", img_src)
                detail_url = driver.current_url

                insert_item.insert_item(conn,name, age, status, full_img_src,detail_url)


                print("상세페이지 주소:", detail_url)
                print("이미지 주소:", full_img_src)
                print("이름:", name)
                print("나이:", age)
                print("대여상태:", status)
                print("-------------------------------")

            # 다음 페이지 링크를 찾고 클릭
            try:
                next_page_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.pagination span.select + a'))
                )
                next_page_button.click()
            except TimeoutException:
                print("마지막 페이지에 도달했습니다.")
                break
finally:
    driver.quit()
    conn.close()