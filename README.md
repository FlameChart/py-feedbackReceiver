# 用户反馈系统 [![wakatime](https://wakatime.com/badge/user/b1cd697f-bbcd-4389-83a2-fe3b452e18fb/project/7df71da7-de75-44e0-89ce-146f332e5e23.svg)](https://wakatime.com/badge/user/b1cd697f-bbcd-4389-83a2-fe3b452e18fb/project/7df71da7-de75-44e0-89ce-146f332e5e23)

一个简单的用户反馈收集系统，支持用户提交反馈并存储到 MySQL 数据库。

## 功能特点

- 用户反馈提交
- MySQL 数据存储
- 环境配置分离
- 跨域支持
- 字数限制和实时计数
- 响应式设计

## 环境要求

- Python 3.8+
- MySQL 5.7+

## 安装步骤

1. 克隆项目到本地

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置环境变量

创建 `.env.dev`（开发环境）或 `.env.prod`（生产环境）文件，包含以下配置：

```bash
DB_HOST=your_mysql_host
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
```

## 运行项目

开发环境：
```bash
python run_dev.py
```

生产环境：
```bash
FLASK_ENV=production python app.py
```

## 接口说明

### 访问首页
- URL: `/`
- 方法: GET
- 请求参数:
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | userId | Integer | 是 | 用户ID | 10001 |
  | username | String | 是 | 用户名 | "张三" |
  | token | String | 是 | 用户认证令牌 | "eyJhbGciOiJ..." |

- 响应: 返回反馈页面 HTML

### 提交反馈
- URL: `/feedback`
- 方法: POST
- Content-Type: `application/json`
- 请求参数:
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | userId | Integer | 是 | 用户ID | 10001 |
  | username | String | 是 | 用户名 | "张三" |
  | content | String | 是 | 反馈内容（最大500字符） | "系统使用体验很好" |

- 响应格式:
```json
{
    "code": Integer,   // 状态码：200成功，400参数错误，401未登录，500服务器错误
    "msg": String,     // 响应消息
    "data": Object     // 响应数据（当前接口返回null）
}
```

- 响应示例:
  - 成功响应:
    ```json
    {
        "code": 200,
        "msg": "反馈提交成功",
        "data": null
    }
    ```
  - 错误响应:
    ```json
    {
        "code": 400,
        "msg": "信息不完整",
        "data": null
    }
    ```

- 错误码说明:
  | 状态码 | 说明 |
  |--------|------|
  | 200 | 成功 |
  | 400 | 参数错误或信息不完整 |
  | 401 | 未登录或登录已过期 |
  | 500 | 服务器内部错误 |

## 注意事项

1. 确保 MySQL 服务已启动且配置正确
2. 数据库表会在首次运行时自动创建
3. 反馈内容最大支持 500 字符
4. 所有环境变量必须正确配置
5. 建议在生产环境使用 WSGI 服务器（如 Gunicorn）
6. 接口调用需要确保参数完整性，所有必填字段都不能为空
7. 建议在请求头中添加 token 用于用户身份验证（如果已实现）

## 数据库表结构

```sql
CREATE TABLE IF NOT EXISTS hsck_feedback (
    id BIGINT AUTO_INCREMENT COMMENT '反馈id' PRIMARY KEY,
    user_id INT NOT NULL COMMENT '用户id',
    username VARCHAR(255) NOT NULL COMMENT '用户名',
    content TEXT NOT NULL COMMENT '反馈内容',
    create_time DATETIME NOT NULL COMMENT '创建时间'
)
```

## 开发相关

- 前端模板位于 `templates/index.html`
- 后端处理逻辑在 `handlers/feedback.py`
- 主应用入口为 `app.py`
