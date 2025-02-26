from app import app
from dotenv import load_dotenv
import os

# 加载开发环境配置
load_dotenv('.env.dev')

if __name__ == '__main__':
    app.run(
        host=os.getenv('HOST', '127.0.0.1'),
        port=int(os.getenv('PORT', 8220)),
        debug=bool(int(os.getenv('FLASK_DEBUG', 1)))
    ) 