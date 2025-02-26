import os
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class FeedbackHandler:
    def __init__(self):
        # 从环境变量获取数据库配置
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
        }
        self._init_table()

    def _init_table(self):
        """初始化反馈表"""
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS hsck_feedback (
            id BIGINT AUTO_INCREMENT COMMENT '反馈id' PRIMARY KEY,
            user_id INT NOT NULL COMMENT '用户id',
            username VARCHAR(255) NOT NULL COMMENT '用户名',
            content TEXT NOT NULL COMMENT '反馈内容',
            create_time DATETIME NOT NULL COMMENT '创建时间'
        )
        """
        
        try:
            cursor.execute(create_table_sql)
            conn.commit()
        except Exception as e:
            print(f"创建表失败: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def add_feedback(self, user_id, username, content):
        """添加反馈"""
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        
        insert_sql = """
        INSERT INTO hsck_feedback (user_id, username, content, create_time)
        VALUES (%s, %s, %s, %s)
        """
        
        try:
            cursor.execute(insert_sql, (
                user_id,
                username,
                content,
                datetime.now()
            ))
            conn.commit()
            return {"code": 200, "message": "反馈提交成功"}
        except Exception as e:
            conn.rollback()
            return {"code": 500, "message": f"反馈提交失败: {str(e)}"}
        finally:
            cursor.close()
            conn.close() 