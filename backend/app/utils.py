from flask_jwt_extended import get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def user_key():
    try:
        identity = get_jwt_identity()
        if identity:  # 用户已登录
            return f"user:{identity}"
    except Exception:
        pass
    return get_remote_address()

limiter = Limiter(
    key_func=user_key,
    storage_uri="redis://redis:6379",
    default_limits=["100 per minute"]
)