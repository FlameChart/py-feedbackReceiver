from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 启用所有跨域请求支持

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True) 