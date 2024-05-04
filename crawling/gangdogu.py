import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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

# 웹 드라이버 초기화
driver = webdriver.Chrome()

urls = [
    "https://www.gdkids.or.kr:8443/imom/02/schedule/schedule.do?toy_gbn=1&co_cd=2",
    "https://www.gdkids.or.kr:8443/imom/05/schedule/schedule.do?toy_gbn=1&co_cd=5",
    "https://www.gdkids.or.kr:8443/imom/07/schedule/schedule.do?toy_gbn=1&co_cd=7",
    "https://www.gdkids.or.kr:8443/imom/03/schedule/schedule.do?toy_gbn=1&co_cd=3",
    "https://www.gdkids.or.kr:8443/imom/06/schedule/schedule.do?toy_gbn=1&co_cd=6"
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
    # 클래스가 contents인 요소 안에 있는 이미지 요소 가져오기
    images = driver.find_elements(By.CSS_SELECTOR, '.album_img_area img')
    
    # 각 이미지를 클릭하고 세부 정보 페이지로 이동하기
    for index, image in enumerate(images):
        # 이미지를 다시 찾아 클릭 (동적 웹페이지 대응)
        current_image = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.album_img_area img'))
        )[index]
        
        try:
            # 이미지 클릭
            current_image.click()
            
            # 세부 정보 페이지로 이동 후 URL 가져오기
            detail_page_url = driver.current_url
            print("Detail page URL:", detail_page_url)

            # 클릭 후 세부 정보 페이지에서 데이터를 가져오는 코드 작성
            get_detail_data()
            
            # 이전 페이지로 이동
            driver.back()
            
            # 페이지가 다시 로드될 때까지 기다리기
            WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.album_img_area img'))
            )
            
        except Exception as e:
            print("An error occurred:", e)

# 세부 정보 페이지에서 이미지와 텍스트 데이터를 가져오는 함수
def get_detail_data():

    # 현재 페이지의 소스를 이용하여 BeautifulSoup 객체 생성
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # 이름 가져오기
    name_tag = soup.select_one("td.bgf4f7fc:contains('장난감/도서명') + td")
    name = name_tag.text.strip() if name_tag else "Name not found"

    # 나이 정보 가져오기
    age_tag = soup.select_one("td.bgf4f7fc:contains('연령') + td")
    age = age_tag.text.strip() if age_tag else "Age not found"

    # 대여 상태 가져오기
    status = "대여가능" if soup.find(text="대여신청") else "예약중"

    # 백그라운드 이미지의 style 속성값 추출
    style_attr = soup.find('div', class_='thumb_img').div['style']
    # 백그라운드 이미지의 URL 추출 (정규표현식 활용)
    background_url = re.search(r"url\('(.*?)'\)", style_attr).group(1)
    img_url = "https://www.gdkids.or.kr:8443"
    full_img_src = urljoin(img_url, background_url)
    detail_url = driver.current_url

    insert_item(conn,name,age,status,full_img_src,detail_url)
    
    print("이미지 주소:", full_img_src)
    print("이름:", name)
    print("나이:", age)
    print("대여상태:", status)
    print("-------------------------------")

# 다음 페이지로 이동하는 함수
def go_to_next_page():
    try:
        # "다음" 링크 찾기
        next_page_link = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.paging_area a.on + a'))
        )
        # 다음 페이지로 이동
        next_page_link.click()
        print("Navigating to next page...")
        # 페이지가 다시 로드될 때까지 기다리기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.album_img_area img'))
        )
        return True
    except Exception as e:
        print("Error navigating to next page:", e)
        return False

# 메인 함수 호출
get_data_and_move_to_next_page()

# 웹 드라이버 종료
driver.quit()
conn.close()