from flask import Flask, request
from flask import render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)

mongo = PyMongo()

client = MongoClient('mongodb://localhost', 27017)   # 로컬환경에서 mongo db 연결

# neuruWeb = 스키마 이름을 Freeitem으로 만듬
db = client.Freeitem

# index 페이지 보여주기
@app.route('/')
def index():
    return render_template('index.html')

# info 페이지 보여주기
@app.route('/info',methods=["GET"])
def info():
    context = db.list.find()
    return render_template('info.html',context=context)

# search 기능
@app.route('/search', methods=["GET"])
def search():
    # GET 요청으로부터 검색어 및 기타 파라미터 가져오기
    domain_seq = request.args.get('domain_seq')
    years_seq = request.args.get('years_seq')
    toy_status = request.args.get('toy_status')
    searchString = request.args.get('searchString')

    # MongoDB 쿼리 작성
    query = {}

    if domain_seq:
        query['domain_seq'] = domain_seq
    if years_seq:
        query['years_seq'] = years_seq
    if toy_status:
        query['toy_status'] = toy_status
    if searchString:
        query['searchString'] = searchString

    # MongoDB에서 검색 결과 가져오기
    results = db.list.find(query)

    return render_template('search.html', results=results)
    

# db write 부분 write.html에서 post로 보낸 데이터 받아서 db에 저장
@app.route('/write', methods=["GET", "POST"])
def board_write():
   if request.method == "POST":
      domain_seq = request.form.get('domain_seq')
      years_seq = request.form.get('years_seq')
      toy_status = request.form.get('toy_status')
      searchString = request.form.get('searchString')
      print(domain_seq, years_seq, toy_status,searchString)
        
      doc = {
         "domain_seq" : domain_seq,
         "years_seq": years_seq,
         "toy_status": toy_status,
         "searchString": searchString,
        }
    # db = neuru web 이라는 스키마임, 스키마 아래에 board라는 컬랙션을 생성후 데이터를 넣음
      db.list.insert_one(doc)

      return render_template("write.html")
   else:
      return render_template("write.html")
       
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)