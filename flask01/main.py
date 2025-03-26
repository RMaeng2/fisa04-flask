from flask import Flask

# 입구 파일을 하나 만들어준다.
app = Flask(__name__)

@app.route('/')
def hello():
    return f'{__name__} hello'

@app.route('/hello3')
def hello2():
    return '두번째'

if __name__ == '__main__':
    app.run(debug=True, port=5001)