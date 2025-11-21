from flask import jsonify
from flask import request
from flask import Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token

from .extension import db

from .models import User


bp = Blueprint('auth', __name__)

# 用户注册
@bp.route('/register', methods=['GET', 'POST'])
def Register():
    # 获取表单信息
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    # 表单验证阶段
    if password != confirm_password:
        return jsonify({"success": False, "message": "两次密码输入不相同!"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"success": False, "message": "该邮箱账号已被注册!"}), 409

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"success": False, "message": "该用户名已经被占用!"}), 409

    # 创建新用户
    user = User()
    user.set_email(email)
    user.set_username(username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"success": True, "message": "账号注册成功!"}), 200


# 用户登录
@bp.route('/api/login', methods=['GET', 'POST'])
def Login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return jsonify({"success": False, "message": "邮箱账号或密码错误!"}), 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    response = jsonify({
        "success": True,
        "access_token": access_token,
        "username": user.username,
        "user_id": user.id,
    })
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=False,  # 本地开发设为False
        samesite="None"
    )

    return response, 200
