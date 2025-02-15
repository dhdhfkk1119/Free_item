from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urljoin
import os
import sys

# insert_item.py 파일의 경로
insert_item_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "insert_item.py"))

# sys.path에 insert_item.py 파일의 경로를 추가하여 모듈을 임포트
sys.path.append(os.path.dirname(insert_item_path))
import insert_item
# DB 연결 가져오기
conn = insert_item.get_db_connection()

# 웹 드라이버 초기화
driver = webdriver.Chrome()

urls = [
    "https://www.ychccic.or.kr/toy/search_toys.htm?p_place=1",
    "https://www.ychccic.or.kr/toy/search_toys.htm?p_place=3",
    "https://www.ychccic.or.kr/toy/search_toys.htm?p_place=4",
    "https://www.ychccic.or.kr/toy/search_toys.htm?p_place=5",
    "https://www.ychccic.or.kr/toy/search_toys.htm?p_place=6",
    "https://www.ychccic.or.kr/toy/search_toys.htm?p_place=8"
]

def get_data_and_move_to_next_page():
    for url in urls:
        try:
            driver.get(url)
            while True:
                click_contents_images_and_get_data()  # 현재 페이지의 정보 가져오기
                if not go_to_next_page():  # 다음 페이지로 이동
                    break  # 다음 페이지로 이동할 수 없으면 종료
        except Exception as e:
            print("An error occurred:", e)
        finally:
            # 현재 URL에서의 정보 수집이 완료되면 다음 URL로 이동
            continue

def click_contents_images_and_get_data():
    # 현재 리스트 페이지의 URL
    current_page_url = driver.current_url

    # 페이지 내의 모든 이미지 요소 가져오기
    images = driver.find_elements(By.CSS_SELECTOR, '.base_cm_noline tbody > tr > td > div > img')
    
    for index, image in enumerate(images):
        # 이미지를 다시 찾아 클릭하기 (동적 웹페이지에 대응하기 위함)
        current_image = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.base_cm_noline tbody > tr > td > div > img'))
        )[index]

        try:
            # 이미지 클릭
            current_image.click()

            # 세부 정보 페이지로 이동 후 데이터 가져오기, 현재 페이지 URL 전달
            get_detail_data(current_page_url)

            # 이전 페이지로 이동
            driver.back()

            # 페이지가 다시 로드될 때까지 기다리기
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.base_cm_noline tbody > tr > td > div > img'))
            )

        except Exception as e:
            print("An error occurred:", e)



def get_detail_data(detail_url):
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # 상품 이름, 나이, 대여 상태, 이미지 URL 가져오기
    name_tag = soup.select_one(".stx20.sblue")
    name = name_tag.text.strip() if name_tag else "Name not found"

    age_tag = soup.find('th', text='연령').find_next_sibling('td')
    age = age_tag.text.strip() if age_tag else "기타"
    if "0세부터" in age:
        age = "0개월이상"
    elif "1세부터" in age:
        age = "12개월이상"        
    elif "2세부터" in age:
        age = "24개월이상"        
    elif "3세이상" in age:
        age = "36개월이상"       
    elif "부모" in age:
        age = "전체연령"     

    status_tags = soup.find('th', text='현재상태').find_next_sibling('td')
    status = status_tags.text.strip() if status_tags else "예약중"
    status = "대여가능" if '보관' in status else "예약중"

    img_tag = soup.select_one("td.ta_center.va_top > img")
    img_src = img_tag.get("src") if img_tag else "Image not found"
    full_img_src = urljoin("https://www.ychccic.or.kr", img_src)

    insert_item.insert_item(conn,name,age,status,full_img_src,detail_url)

    # 출력 또는 데이터베이스 저장
    print("List Page URL:", detail_url)
    print("Image URL:", full_img_src)
    print("Name:", name)
    print("Age:", age)
    print("Rental Status:", status)
    print("-------------------------------")


# "다음 페이지로 이동하는 함수"
def go_to_next_page():
    try:
        # "다음" 링크 찾기
        next_page_link = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//li[@class="on"]/following-sibling::li'))
        )
        # 다음 페이지로 이동
        next_page_link.click()

        return True
    except:
        return False

# 메인 함수 호출
get_data_and_move_to_next_page()
# 웹 드라이버 종료
driver.quit()
conn.close()