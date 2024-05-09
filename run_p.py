import runpy
import sys
import os

# 현재 스크립트의 디렉토리 경로를 가져옴
current_dir = os.path.dirname(os.path.realpath(__file__))
# insert_item.py 파일이 있는 디렉토리를 모듈 검색 경로에 추가
insert_item_dir = os.path.join(current_dir, "crawling")
sys.path.append(insert_item_dir)

#크롤링하는 파이썬 코드 실행 

#기존에 있던 item 데이터 삭제 
runpy.run_path("delete_data.py")
# #크롤링해서 데이터 가져오기 
# runpy.run_path("crawling/gangseo.py")
#웹 서버 열기 
# Flask 애플리케이션 실행
runpy.run_path("app.py")


# runpy.run_path("crawling/dongcci.py")
# runpy.run_path("crawling/gangdogu.py")
# runpy.run_path("crawling/gangnamgu.py")
# runpy.run_path("crawling/geumcheon.py")
# runpy.run_path("crawling/gurogu.py")
# runpy.run_path("crawling/gwanak.py")
# runpy.run_path("crawling/mapogu.py")
# runpy.run_path("crawling/namukey.py")
# runpy.run_path("crawling/seocho.py")
# runpy.run_path("crawling/seodemun.py")
# runpy.run_path("crawling/songpagu.py")
# runpy.run_path("crawling/yangcheon.py")
# runpy.run_path("crawling/Yeongdeungpo.py")
