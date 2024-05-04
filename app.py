from flask import Flask, render_template, request
import pymysql
import pymysql.cursors

app = Flask(__name__)

def get_db_connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        db='toy',
        charset='utf8'
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info', methods=["GET"])
def info():
    conn = get_db_connection()
    curs = conn.cursor(pymysql.cursors.DictCursor)

    # 게시물의 총 수를 조회
    curs.execute("SELECT COUNT(*) AS total FROM item")
    total_posts = curs.fetchone()['total']

    # 게시물 데이터 조회
    curs.execute("SELECT idx, name, age, status, img_src, detail_url FROM item")
    items = curs.fetchall()

    curs.close()
    conn.close()

    return render_template('info.html', items=items, total_posts=total_posts)

@app.route('/search',methods=["GET"])
def search():
    # 검색 파라미터 받기
    domain_seq = request.args.get('domain_seq')
    years_seq = request.args.get('years_seq')
    toy_status = request.args.get('toy_status')
    searchString = request.args.get('searchString')

    #데이터베이스 연결
    conn = get_db_connection()
    curs = conn.cursor(pymysql.cursors.DictCursor)

    # 기본 검색 쿼리
    query = "SELECT idx, name, age, status, img_src, detail_url FROM item WHERE 1=1"
    
    # 조건 추가
    conditions = []
    if domain_seq:
        conditions.append("domain_seq = %s")
    if years_seq:
        conditions.append("years_seq = %s")
    if toy_status:
        conditions.append("status = %s")
    if searchString:
        conditions.append("(name LIKE %s OR idx = %s)")

    # 쿼리에 조건 추가
    if conditions:
        query += ' AND ' + ' AND '.join(conditions)

    # 실행할 쿼리 파라미터
    params = [param for param in (domain_seq, years_seq, toy_status, f"%{searchString}%", searchString) if param]

    # 쿼리 실행
    curs.execute(query, params)
    results = curs.fetchall()

    curs.close()
    conn.close()

    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
