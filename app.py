from flask import Flask
from flask_migrate import Migrate
from database import db
from models.users import User
from flask import request
from flask import jsonify
from sqlalchemy import select
from schemas.user import UserCreateSchema, UserUpdateSchema
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flasgger import Swagger
from log_config import setup_logging
from loguru import logger
from swagger import swagger_config, template

setup_logging()
app = Flask(__name__)

# Initialize database configuration.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "flask-jwt-secret"

# Initialize the database and migration objects.
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
swagger = Swagger(app, config=swagger_config, template=template)

# Define response objects.
class ResponseObject:
    def __init__(self, message: str, data=None, code: int = 200):
        self.message = message
        self.data = data
        self.code = code

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }


# Define api routes.
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods=["POST"])
def login():
    """
    用户登录
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: test@example.com
            password:
              type: string
              example: 123456
    responses:
      200:
        description: 登录成功，返回 Token
        schema:
          type: object
          properties:
            access_token:
              type: string
      401:
        description: 账号或密码错误
    """
    email = request.json.get("email")
    password = request.json.get("password")

    stmt = select(User).where(User.email == email)
    user = db.session.execute(stmt).scalars().first()

    if not user or not user.check_password(password):
        return jsonify(ResponseObject("Invalid email or password", code=401).to_dict()) 
    
    access_token = create_access_token(identity=str(user.id))
    logger.success(f"User {user.id} logged in successfully.")
    return jsonify(ResponseObject("Login successful", {"access_token": access_token}).to_dict())

@app.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    """
    获取用户列表
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: query
        name: keyword
        type: string
        required: false
        description: 关键词搜索用户名称
    responses:
      200:
        description: 成功获取用户列表
        schema:
          type: object
          properties:
            code:
              type: integer
            message:
              type: string
            data:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                email:
                  type: string
                first_name:
                  type: string
                last_name:
                  type: string
                description:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
    """
    users = select(User)
    try:
        keyword = request.args.get("keyword", "")
        if keyword:
            users = users.where(User.name.contains(keyword))
        else:
            users = users.limit(10)
        result = db.session.execute(users).scalars().all()
        logger.info(f"Retrieved {len(result)} users.")
        return jsonify(ResponseObject("Success", [user.to_dict() for user in result]).to_dict())
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return jsonify(ResponseObject("Error", code=500).to_dict())

@app.route("/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_info(user_id):
    """
    获取用户信息
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: 用户ID
    responses:
      200:
        description: 成功获取用户信息
        schema:
          type: object
          properties:
            code:
              type: integer
            message:
              type: string
            data:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                email:
                  type: string
                first_name:
                  type: string
                last_name:
                  type: string
                description:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
    """
    user = db.session.get(User, user_id)
    if not user:
        logger.error(f"User with id {user_id} not found.")
        return jsonify(ResponseObject("User not found", code=404).to_dict())
    logger.success(f"User {user.id} retrieved successfully.")
    return jsonify(ResponseObject("Success", user.to_dict()).to_dict())

@app.route("/users", methods=["POST"])
@jwt_required()
def create_user():
    """
    创建新用户
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        description: 用户注册信息
        required: true
        schema:
          type: object
          required:
            - email
            - name
            - password
          properties:
            email:
              type: string
            name:
              type: string
            password:
              type: string
            description:
              type: string
    responses:
      200:
        description: 用户创建成功
      422:
        description: 参数验证失败
    """
    form_data = request.form.to_dict()
    validated_data = UserCreateSchema(**form_data)
    user = User()
    user.email = validated_data.email
    user.name = validated_data.name
    user.first_name = validated_data.first_name
    user.last_name = validated_data.last_name
    user.description = validated_data.description
    user.set_password(validated_data.password)

    try:
        # Check if user with same email or name exists.
        if check_user_exists(user.email, user.name):
            return jsonify(ResponseObject("User with the same email or name already exists", code=400).to_dict())
        db.session.add(user)
        db.session.commit()
        return jsonify(ResponseObject("User created successfully", user.to_dict()).to_dict())
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error occurred while checking user existence: {e}")
        return jsonify(ResponseObject("Error", code=500).to_dict())
   
@app.route("/user/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    """
    更新用户信息
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: 用户ID
      - in: body
        name: body
        description: 用户更新信息
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            name:
              type: string
            first_name:
              type: string
            last_name:
              type: string
            description:
              type: string
    responses:
      200:
        description: 用户信息更新成功
      404:
        description: 用户未找到
      422:
        description: 参数验证失败
    """
    user = db.session.get(User, user_id)
    if not user:
        return jsonify(ResponseObject("User not found", code=404).to_dict())
    try:
        # TODO: Update user fields based on request data.
        form_data = request.form.to_dict()
        validated_data = UserUpdateSchema(**form_data)
        clean_data = validated_data.model_dump(exclude_unset=True)
        for key, value in clean_data.items():
            # setattr(对象, 属性名, 属性值) 相当于 user.key = value
            setattr(user, key, value)
        db.session.commit()
        return jsonify(ResponseObject("User updated successfully", user.to_dict()).to_dict())
    except Exception as e:
        logger.error(f"Error occurred while updating user: {e}")
        db.session.rollback()
        return jsonify(ResponseObject("Error", code=500).to_dict())

@app.route("/change_password/<int:user_id>", methods=["POST"])
@jwt_required()
def change_user_password(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify(ResponseObject("User not found", code=404).to_dict())
    try:
        # TODO: Update user fields based on request data.
        password = request.form["password"]
        user.set_password(password)
        db.session.commit()
        return jsonify(ResponseObject("User updated successfully", user.to_dict()).to_dict())
    except Exception as e:
        logger.error(f"Error occurred while updating user: {e}")
        db.session.rollback()
        return jsonify(ResponseObject("Error", code=500).to_dict())

@app.route("/user/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    """
    删除用户
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: 用户ID
    responses:
      200:
        description: 用户删除成功
      404:
        description: 用户未找到
    """
    user = db.session.get(User, user_id)
    if not user:
        return jsonify(ResponseObject("User not found", code=404).to_dict())
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify(ResponseObject("User deleted successfully").to_dict())
    except Exception as e:
        logger.error(f"Error occurred while deleting user: {e}")
        db.session.rollback()
        return jsonify(ResponseObject("Error", code=500).to_dict())

def check_user_exists(email: str, name: str) -> bool:
    user_query = select(User).where((User.email == email) | (User.name == name))
    existing_user = db.session.execute(user_query).scalar_one_or_none()
    return existing_user is not None

if __name__ == "__main__":
    app.run(debug=True)