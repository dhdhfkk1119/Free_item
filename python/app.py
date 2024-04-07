from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index')
def register():
    return render_template('index.html')

@app.route('/info')
def hello_world():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)