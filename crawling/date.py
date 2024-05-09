import concurrent.futures
import subprocess

# 실행할 파이썬 스크립트 파일 목록
scripts = [
    'dongccic.py', 'gangdogu.py', 'gangnamgu.py', 'gangseo.py', 'geumcheon.py', 'gurogu.py', 'gwanak.py',
    'mapogu.py', 'namukey.py', 'seoch.py', 'seodemun.py', 'songpagu.py', 'yangcheon.py', 'Yeongdeungpo.py'
]

# 각 스크립트를 실행하는 함수
def run_script(script):
    subprocess.run(['python', script])

# 최대 스레드 수 설정
max_threads = min(len(scripts), 14)  # 14개의 스크립트와 같은 수의 스레드로 실행

# 병렬 처리
with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    executor.map(run_script, scripts)
