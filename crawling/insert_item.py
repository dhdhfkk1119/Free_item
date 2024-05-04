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

def insert_item(conn, name, age, status, full_img_src, detail_url):
    try:
        with conn.cursor() as cursor:
            # SQL 문 실행
            sql = "INSERT INTO item (name, age, status, img_src, detail_url) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, age, status, full_img_src, detail_url))
        # 변경사항 저장
        conn.commit()
    except Exception as e:
        print("Error inserting item:", e)
