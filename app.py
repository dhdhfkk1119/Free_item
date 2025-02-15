from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors
import pymysql
from flask import jsonify
import re

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

def extract_number(text):
    pattern = r'\b\d+\b'
    matches = re.findall(pattern, text)
    if matches:
        return int(matches[0])
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info', methods=["GET"])
def info():
    # 현재 페이지 및 페이지당 상품 수
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 36, type=int)  # 기본값 25

    conn = get_db_connection()
    curs = conn.cursor(pymysql.cursors.DictCursor)

    # 전체 게시물 수 조회
    curs.execute("SELECT COUNT(*) AS total FROM item")
    total_posts = curs.fetchone()['total']

    # 페이지당 게시물 조회
    curs.execute("SELECT idx, name, age, status, img_src, detail_url FROM item LIMIT %s OFFSET %s", (per_page, (page - 1) * per_page))
    items = curs.fetchall()

    curs.close()
    conn.close()

    return render_template('info.html', items=items, total_posts=total_posts, page=page, per_page=per_page)

@app.route('/increase_view_count', methods=["POST"])
def increase_view_count():
    if request.method == 'POST':
        item_id = request.form['item_id']

        conn = get_db_connection()
        curs = conn.cursor()

        # 상품의 조회수 증가 처리
        curs.execute("UPDATE item SET views = views + 1 WHERE idx = %s", (item_id,))
        conn.commit()

        curs.close()
        conn.close()

        return jsonify({'message': 'View count increased successfully'}), 200
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/sort_items', methods=["POST"])
def sort_items():
    if request.method == 'POST':
        sort_by = request.form['sort_by']

        conn = get_db_connection()
        curs = conn.cursor(pymysql.cursors.DictCursor)

        if sort_by == 'view_count':
            # 조회수가 높은 순으로 상품 조회
            curs.execute("SELECT idx, name, age, status, img_src, detail_url FROM item ORDER BY views DESC")
        else:
            # 기본 정렬 (원하는 방식으로 변경)
            curs.execute("SELECT idx, name, age, status, img_src, detail_url FROM item ORDER BY created_at DESC")

        items = curs.fetchall()

        curs.close()
        conn.close()

        # 정렬된 결과를 JSON 형식으로 반환
        return jsonify({'items': items}), 200
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/search', methods=["GET"])
def search():
    age = request.args.get('age')
    status = request.args.get('status')
    searchString = request.args.get('searchString')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 36, type=int)

    conn = get_db_connection()
    curs = conn.cursor(pymysql.cursors.DictCursor)

    query = "SELECT idx, name, age, status, img_src, detail_url FROM item WHERE 1=1"
    params = []

    # 조건 추가
    if age and age != 'none':
        age_number = extract_number(age)
        if age_number is not None:
            query += " AND age >= %s"
            params.append(age_number)
        elif age == '전체':
            query += " AND age LIKE %s"
            params.append('%전체%')
        elif age == '기타':
            query += " AND age LIKE %s"
            params.append('%기타%')
        else:
            age_number = extract_number(age)
            if age_number is not None:
                query += " AND age >= %s"
                params.append(age_number)
            else:
                query += " AND age = %s"
                params.append(age)

    if status and status != "none":
        query += " AND status = %s"
        params.append(status)

    if searchString:
        query += " AND (name LIKE %s OR idx = %s)"
        params.extend([f"%{searchString}%", searchString])

    # 페이징을 위한 쿼리 수정
    total_query = "SELECT COUNT(*) AS total FROM item WHERE " + query[query.index("WHERE")+6:]
    curs.execute(total_query, params)
    total_posts = curs.fetchone()['total']

    # 페이지네이션 적용
    query += " LIMIT %s OFFSET %s"
    params.extend([per_page, (page - 1) * per_page])

    # 쿼리 실행
    curs.execute(query, params)
    items = curs.fetchall()

    curs.close()
    conn.close()

    # 다음 페이지로 넘어갈 때, 현재 페이지와 관련된 검색 조건을 다음 페이지로도 함께 전달
    next_page = page + 1 if (page * per_page) < total_posts else None
    return render_template('search.html', items=items, total_posts=total_posts, page=page, per_page=per_page, next_page=next_page, age=age, status=status, searchString=searchString)


if __name__ == '__main__':
    app.run(host='175.199.193.175', port=5000, debug=True)
