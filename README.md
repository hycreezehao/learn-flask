# 🚀 Flask User Management API（Demo）

一个基于 **Flask + SQLAlchemy + JWT + Swagger + Pydantic** 的用户管理
API Demo。\
该项目展示了一个可扩展、可维护、工程化的 Flask 后端服务结构，可作为学习
Flask 或构建内部工具的基础模板。

------------------------------------------------------------------------

## 📌 Features 功能特性

-   ✅ 用户登录（JWT）\
-   ✅ 用户 CRUD（创建、查询、更新、删除）\
-   ✅ 参数校验（Pydantic）\
-   ✅ Swagger API 文档（Flasgger）\
-   ✅ SQLite + SQLAlchemy ORM\
-   ✅ Loguru 日志系统\
-   ✅ RESTful 风格接口\
-   ✅ 可扩展的项目结构

适合作为：

-   企业内部 API demo\
-   Flask 学习模板\
-   小型管理工具后台\
-   Python Web 项目入门

------------------------------------------------------------------------

## 📂 Project Structure 项目结构

    project/
    │── app.py                  # 主应用入口
    │── database.py             # 数据库初始化
    │── log_config.py           # 日志配置
    │── swagger.py              # Swagger 配置
    │── models/
    │     └── users.py          # 用户 Model
    │── schemas/
    │     └── user.py           # Pydantic 参数校验

------------------------------------------------------------------------

## 🔧 Installation & Setup 安装与运行

### 1️⃣ 创建虚拟环境（可选）

``` bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

### 2️⃣ 安装依赖

``` bash
pip install -r requirements.txt
```

### 3️⃣ 初始化数据库

``` bash
flask db init
flask db migrate
flask db upgrade
```

### 4️⃣ 启动服务

``` bash
python app.py
```

访问 Swagger 文档：\
👉 http://localhost:5000/apidocs

------------------------------------------------------------------------

## 🔐 Authentication 认证机制（JWT）

登录接口：\
`POST /login`

成功后会返回：

``` json
{
  "code": 200,
  "message": "Login successful",
  "data": {
    "access_token": "xxxxxx"
  }
}
```

后续所有需要认证的接口需携带 Token：

    Authorization: Bearer <token>

Swagger 页面右上角有 "Authorize" 按钮可直接填写。

------------------------------------------------------------------------

## 📚 API Summary（简要）

  Method   Endpoint     Description
  -------- ------------ ------------------
  POST     /login       用户登录
  GET      /users       获取用户列表
  POST     /users       创建用户
  GET      /user/{id}   获取单个用户信息
  PUT      /user/{id}   更新用户
  DELETE   /user/{id}   删除用户

------------------------------------------------------------------------

## 🧪 Tech Stack 技术栈

-   **Flask** --- Web 框架\
-   **Flasgger** --- 自动化 API 文档\
-   **SQLAlchemy** --- ORM\
-   **SQLite** --- Demo 数据库\
-   **JWT (flask-jwt-extended)** --- 身份认证\
-   **Pydantic** --- 参数验证\
-   **Loguru** --- 日志系统

------------------------------------------------------------------------

## 📄 License

MIT License.

------------------------------------------------------------------------

## 🎉 Thanks

如果你喜欢这个 Demo，欢迎 Star ⭐️！
