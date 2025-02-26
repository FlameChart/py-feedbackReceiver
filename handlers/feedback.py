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
        self._init_database()
        self._init_table()

    def _init_database(self):
        """初始化数据库"""
        try:
            # 创建没有指定数据库的连接
            conn = mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            cursor = conn.cursor()
            
            # 创建数据库
            create_db_sql = f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}"
            cursor.execute(create_db_sql)
            conn.commit()
            
        except mysql.connector.Error as e:
            print(f"[Database Init] 数据库连接失败: {str(e)}")
            print("[Database Init] 请检查MySQL服务是否启动，以及数据库配置是否正确")
            import sys
            sys.exit(1)
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def _init_table(self):
        """初始化反馈表"""
        try:
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
            
            cursor.execute(create_table_sql)
            conn.commit()
        except mysql.connector.Error as e:
            print(f"[Table Init] 数据库连接失败: {str(e)}")
            print("[Table Init] 请检查MySQL服务是否启动，以及数据库配置是否正确")
            import sys
            sys.exit(1)
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def add_feedback(self, user_id, username, content):
        """添加反馈"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            insert_sql = """
            INSERT INTO hsck_feedback (user_id, username, content, create_time)
            VALUES (%s, %s, %s, %s)
            """
            
            cursor.execute(insert_sql, (
                user_id,
                username,
                content,
                datetime.now()
            ))
            conn.commit()
            return {"code": 200, "message": "反馈提交成功"}
        except mysql.connector.Error as e:
            if 'conn' in locals():
                conn.rollback()
            print(f"[Feedback Operation] 数据库操作失败: {str(e)}")
            return {"code": 500, "message": f"反馈提交失败: {str(e)}"}
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close() 