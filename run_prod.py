from app import app
from dotenv import load_dotenv
import os

# 加载生产环境配置
load_dotenv('.env.prod')

if __name__ == '__main__':
    if os.getenv('SSL_ENABLED', '0') == '1':
        app.run(
            host=os.getenv('HOST', '0.0.0.0'),
            port=int(os.getenv('PORT', 443)),
            debug=bool(int(os.getenv('FLASK_DEBUG', 0))),
            ssl_context=(os.getenv('SSL_CERT_PATH'), os.getenv('SSL_KEY_PATH'))
        )
        exit()
    else:
        app.run(
            host=os.getenv('HOST', '0.0.0.0'),
            port=int(os.getenv('PORT', 8000)),
            debug=bool(int(os.getenv('FLASK_DEBUG', 0)))
        )