import pymysql

def get_db_connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        db='toy',
        charset='utf8'
    )
    return conn

def delete_all_data():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # toy 데이터베이스의 모든 테이블에서 데이터 삭제
            cursor.execute("DELETE FROM item")
            # 필요한 만큼 다른 테이블에 대해서도 위와 같은 방식으로 삭제 진행

        # 변경사항을 커밋
        conn.commit()
        print("모든 데이터가 삭제되었습니다.")
    finally:
        # 연결 종료
        conn.close()

# 모든 데이터 삭제 함수 호출
delete_all_data()
