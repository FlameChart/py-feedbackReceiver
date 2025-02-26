from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from handlers.feedback import FeedbackHandler

# 根据环境变量加载对应的配置文件
env = os.getenv('FLASK_ENV', 'development')
if env == 'production':
    load_dotenv('.env.prod')
else:
    load_dotenv('.env.dev')

app = Flask(__name__)
CORS(app)  # 启用所有跨域请求支持

# 初始化 FeedbackHandler
feedback_handler = FeedbackHandler()

@app.route('/')
def feedback_page():
    return render_template('index.html')

@app.route('/api/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    content = data.get('content')
    
    if not content or not content.strip():
        return jsonify({'error': '反馈内容不能为空'}), 400
        
    # 这里可以添加保存反馈到数据库的逻辑
    
    return jsonify({'message': '反馈提交成功'}), 200

@app.route('/feedback', methods=['POST'])
def handle_feedback():
    data = request.get_json()
    
    # 验证必要字段
    required_fields = ['userId', 'username', 'content']
    if not all(field in data for field in required_fields):
        return jsonify({"code": 400, "message": "缺少必要字段"}), 400
    
    # 调用 handler 处理反馈
    result = feedback_handler.add_feedback(
        user_id=data['userId'],
        username=data['username'],
        content=data['content']
    )
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 