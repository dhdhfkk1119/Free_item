from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urljoin

# 웹 드라이버 초기화
driver = webdriver.Chrome()

# 웹 페이지 로드
driver.get("https://bcsclib.egentouch.com/search.do?action=totalSearchResultList&fix_material_type=t&menuid=j1_6")

# 클래스가 contents인 요소 안에 있는 이미지를 클릭하고 세부 정보 페이지로 이동하는 함수
def click_contents_images_and_get_data():
    # 클래스가 contents인 요소 안에 있는 이미지 요소 가져오기
    images = driver.find_elements(By.CSS_SELECTOR, '.doc_body > ul > li')
    
    # 각 이미지를 클릭하고 세부 정보 페이지로 이동하기
    for index, image in enumerate(images):
        # 이미지를 다시 찾아 클릭 (동적 웹페이지 대응)
        current_image = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.doc_body > ul > li'))
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
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.doc_body > ul > li'))
            )

        except Exception as e:
            print("An error occurred:", e)


# 세부 정보 페이지에서 이미지와 텍스트 데이터를 가져오는 함수
def get_detail_data():

    # 현재 페이지의 소스를 이용하여 BeautifulSoup 객체 생성
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # 이름 가져오기
    name_tag = soup.select_one(".info_title")
    name = name_tag.text.strip() if name_tag else "Name not found"

    # 나이 정보 가져오기
    age_tag = soup.find('p',text='사용연령').find_next_sibling('p')
    age = age_tag.text.strip() if age_tag else "Age not found"

    # 대여 상태 가져오기
    status_text = ""
    table_rows = soup.select("tbody tr")
    for row in table_rows:
        status_element = row.find("td", style="color:blue")
        if status_element and '대출가능' in status_element.text.strip():
            status_text = "대여가능"
            break
    else:
        status_text = "예약중"


    # 이미지 주소 가져오기
    img_tag = soup.select_one(".image_area > img")
    img_src = img_tag.get("src") if img_tag else "Image not found"

    print("이미지 주소:", img_src)
    print("이름:", name)
    print("나이:", age)
    print("대여상태:", status_text)
    print("-------------------------------")

# "다음 페이지로 이동하는 함수"
def go_to_next_page():
    try:
        # 현재 페이지의 HTML을 가져와 BeautifulSoup 객체를 생성합니다.
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 현재 선택된 페이지 번호를 가져옵니다.
        current_page = int(soup.select_one("a.on").text)

        # 다음 페이지 번호를 계산합니다.
        next_page = current_page + 1
        # 다음 페이지 번호를 가진 링크를 찾습니다.
        next_page_link = driver.find_element(By.XPATH, f"//a[contains(@onclick, 'fn_link_page') and contains(@onclick, '{next_page}')]")
        next_page_link.click()

        return True
    except:
        return False


# 한 페이지에 대한 정보를 얻고 다음 페이지로 이동하는 메인 함수
def get_data_and_move_to_next_page():
    try:
        while True:
            click_contents_images_and_get_data()  # 현재 페이지의 정보 가져오기
            if not go_to_next_page():  # 다음 페이지로 이동
                break  # 다음 페이지로 이동할 수 없으면 종료
    finally:
        # 웹 드라이버 종료
        print("마지막페이지 입니다.")
        driver.quit()

# 메인 함수 호출
get_data_and_move_to_next_page()
