import bcrypt
from flask import Blueprint, request, jsonify
from db_manager import DBManager

# 原业务类保留
class UserService:
    def __init__(self, db: DBManager):
        self.db = db

    def register(self, username, password, role='customer'):
        salt = bcrypt.gensalt()
        pw_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        sql = "INSERT INTO user (USERNAME, PASSWORD_HASH, ROLE) VALUES (%s, %s, %s)"
        cursor = self.db.execute(sql, (username, pw_hash, role))
        return cursor is not None

    def login(self, username, password):
        sql = "SELECT * FROM user WHERE USERNAME = %s"
        cursor = self.db.execute(sql, (username,))
        user = cursor.fetchone() if cursor else None

        if user:
            hashed = user['PASSWORD_HASH'].encode('utf-8')  # 数据库存的是加密密码
            if bcrypt.checkpw(password.encode('utf-8'), hashed):
                print("登录成功！")
                return user  # 登录成功，返回用户数据
            else:
                print("密码错误！")
        else:
            print("用户不存在！")
        return None


# ========== 以下为 Web API 蓝图部分 ==========
user_bp = Blueprint('user', __name__)
user_svc = UserService(DBManager())

@user_bp.route('/register', methods=['POST'])
def register_api():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "customer")
    success = user_svc.register(username, password, role)
    if success:
        return jsonify({"message": "注册成功"}), 201
    else:
        return jsonify({"error": "注册失败，可能用户名已存在"}), 400

@user_bp.route('/login', methods=['POST'])
def login_api():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = user_svc.login(username, password)
    if user:
        return jsonify({
            "uid": user["UID"],
            "username": user["USERNAME"],
            "role": user["ROLE"]
        }), 200
    else:
        return jsonify({"error": "用户名或密码错误"}), 401
