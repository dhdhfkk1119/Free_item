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

# 웹 페이지 로드
urls = [
    "https://www.happycare.or.kr/html/sub/index_toy.php?pno=22010101&page=1",
    "https://www.happycare.or.kr/html/sub/index_toy.php?pno=22020101"
]

# 한 페이지에 대한 정보를 얻고 다음 페이지로 이동하는 메인 함수
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

# 클래스가 contents인 요소 안에 있는 이미지를 클릭하고 세부 정보 페이지로 이동하는 함수
def click_contents_images_and_get_data():
    # 클래스가 contents인 요소 안에 있는 이미지 요소 가져오기
    images = driver.find_elements(By.CSS_SELECTOR, 'ul.toy_list > li a')
    
    # 각 이미지를 클릭하고 세부 정보 페이지로 이동하기
    for index, image in enumerate(images):
        # 이미지를 다시 찾아 클릭 (동적 웹페이지 대응)
        current_image = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.toy_list > li a'))
        )[index]
        try:
            # 토이 클릭
            current_image.click()

            # 세부 정보 페이지로 이동 후 URL 가져오기
            detail_page_url = driver.current_url
            print("Detail page URL:", detail_page_url)

            # 클릭 후 세부 정보 페이지에서 데이터를 가져오는 코드 작성
            get_detail_data()

            # 이전 페이지로 이동
            driver.back()

            # 페이지가 다시 로드될 때까지 기다리기
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.toy_list > li a'))
            )

        except Exception as e:
            print("An error occurred:", e)


# 세부 정보 페이지에서 이미지와 텍스트 데이터를 가져오는 함수
def get_detail_data():

    # 현재 페이지의 소스를 이용하여 BeautifulSoup 객체 생성
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # 이름 가져오기
    name_tag = soup.find('th', text='장난감명').find_next_sibling('td')
    name = name_tag.text.strip() if name_tag else "Name not found"

    # 나이 정보 가져오기
    age_tag = soup.find('th',text='연령').find_next_sibling('td')
    age = age_tag.text.strip() if age_tag else "Age not found"
    if "0세이상" in age:
        age = "0개월이상"
    elif "1세이상" in age:
        age = "12개월이상"        
    elif "2세이상" in age:
        age = "24개월이상"        
    elif "3세이상" in age:
        age = "36개월이상"        
    elif "4세이상" in age:
        age = "48개월이상"
    elif "5세이상" in age:
        age = "5세이상"                        
    elif "6세이상" in age:
        age = "6세이상"
    elif "7세이상" in age:
        age = "7세이상"    
                    
    # 대여 상태 가져오기
    status_tags = soup.select_one("span.toy_state")
    status = status_tags.text.strip() if status_tags else "Not status_tage"
    if "대여가능" in status:
        status = "대여가능"
    else :
        status = "예약중"

    # 이미지 주소 가져오기
    img_tag = soup.select_one("dl.toyView > dt > img")
    img_src = img_tag.get("src") if img_tag else "Image not found"
    img_url = "https://www.happycare.or.kr/"
    full_img_src = urljoin(img_url, img_src)
    detail_url = driver.current_url

    insert_item.insert_item(conn,name,age,status,full_img_src,detail_url)

    print("이미지 주소:", full_img_src)
    print("이름:", name)
    print("나이:", age)
    print("대여상태:", status)
    print("-------------------------------")

# "다음 페이지로 이동하는 함수"
def go_to_next_page():
    try:
        # "다음" 링크 찾기
        next_page_link = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="select"]/following-sibling::span'))
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