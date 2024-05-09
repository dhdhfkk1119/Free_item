from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors
import pymysql
from flask import jsonify

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


if __name__ == '__main__':
    app.run(debug=True)
