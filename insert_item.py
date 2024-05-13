import pymysql
import datetime


def get_db_connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        db='toy',
        charset='utf8'
    )
    return conn

def insert_item(conn, name, age, status, full_img_src, detail_url):
    try:
        created_at = datetime.datetime.now()  # 현재 시간을 가져옵니다.
        with conn.cursor() as cursor:
            # 상품 정보 확인
            cursor.execute("SELECT status FROM item WHERE name = %s AND age = %s", (name, age))
            result = cursor.fetchone()
            
            if result:
                # 상품이 이미 존재하면 상태를 확인
                current_status = result[0]
                if current_status != status:
                    # 상태가 다르면 상태와 created_at만 업데이트
                    cursor.execute("UPDATE item SET status = %s, created_at = %s WHERE name = %s AND age = %s",
                                   (status, created_at, name, age))
            else:
                # 상품이 없으면 새로 삽입
                sql = "INSERT INTO item (name, age, status, img_src, detail_url, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, age, status, full_img_src, detail_url, created_at))

        # 변경사항 저장
        conn.commit()
    except Exception as e:
        print("Error updating or inserting item:", e)