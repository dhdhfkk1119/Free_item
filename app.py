from flask import Flask, request
from flask import render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)

mongo = PyMongo()

client = MongoClient('mongodb://localhost', 27017)   # 로컬환경에서 mongo db 연결
# client = MongoClient('mongodb://test:test@localhost', 27017)    # db 인증 계정 생성 후 연결 방법

# neuruWeb = 스키마 이름을 느루웹으로 만듬
db = client.Freeitem

@app.route('/')

# db write 부분 write.html에서 post로 보낸 데이터 받아서 db에 저장
@app.route('/write', methods=["GET", "POST"])
def board_write():
   if request.method == "POST":
      name = request.form.get("name")
      title = request.form.get("title")
      contents = request.form.get("contents")
      print(name, title, contents)
        
      doc = {
         "name": name,
         "title": title,
         "contents": contents,
        }
    # db = neuru web 이라는 스키마임, 스키마 아래에 board라는 컬랙션을 생성후 데이터를 넣음
      db.board.insert_one(doc)

      return render_template("write.html")
   else:
      return render_template("write.html")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)