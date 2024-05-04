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
    "https://www.gwanak-toy.or.kr/front/index.php?g_page=search&m_page=search01"
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


# "다음 페이지로 이동하는 함수"
def go_to_next_page():
    try:
        # "다음" 링크 찾기
        next_page_link = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.paging strong + a'))
        )
        # 다음 페이지로 이동
        next_page_link.click()

        return True
    except:
        return False

# 클래스가 contents인 요소 안에 있는 이미지를 클릭하고 세부 정보 페이지로 이동하는 함수
def click_contents_images_and_get_data():
    # 클래스가 contents인 요소 안에 있는 이미지 요소 가져오기
    images = driver.find_elements(By.CSS_SELECTOR, '.toy_search_list > ul > li > a')
    
    # 각 이미지를 클릭하고 세부 정보 페이지로 이동하기
    for index, image in enumerate(images):
        # 이미지를 다시 찾아 클릭 (동적 웹페이지 대응)
        current_image = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.toy_search_list > ul > li:nth-of-type({}) > a'.format(index + 1)))
        )
        
        try:
            # 토이 클릭
            current_image.click()

            # 세부 정보 페이지로 이동 후 URL 가져오기
            detail_url = driver.current_url
            print("Detail page URL:", detail_url)

            # 클릭 후 세부 정보 페이지에서 데이터를 가져오는 코드 작성
            get_detail_data()

            # 이전 페이지로 이동
            driver.back()

            # 페이지가 다시 로드될 때까지 기다리기
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.toy_search_list > ul > li > a'))
            )

        except Exception as e:
            print("An error occurred:", e)


# 세부 정보 페이지에서 이미지와 텍스트 데이터를 가져오는 함수
def get_detail_data():

    # 현재 페이지의 소스를 이용하여 BeautifulSoup 객체 생성
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # 이름 가져오기
    name_tag = soup.select_one("div.tvi_txt > dl > dt")
    name = name_tag.text.strip() if name_tag else "Name not found"

    # 나이 정보 가져오기
    age_tag = soup.select_one("div.tvi_txt > ul > li:contains('전체')")
    age = age_tag.text.strip() if age_tag else "Age not found"

    # 대여 상태 가져오기
    status_tags = soup.select("div.tvi_txt > dl > dd > span.con")
    status = "대여중" if any(tag.text.strip() == "0" for tag in status_tags) else "대여가능"
    
    # 이미지 주소 가져오기
    img_tag = soup.select_one("div.tvi_img > img")
    img_src = img_tag.get("src") if img_tag else "Image not found"
    img_url = "https://www.gwanak-toy.or.kr"
    full_img_src = urljoin(img_url, img_src)
    detail_url = driver.current_url

    insert_item(conn,name, age, status, full_img_src,detail_url)

    print("이미지 주소:", full_img_src)
    print("이름:", name)
    print("나이:", age)
    print("대여상태:", status)
    print("-------------------------------")



# 메인 함수 호출
get_data_and_move_to_next_page()
# 웹 드라이버 종료
driver.quit()
conn.close()