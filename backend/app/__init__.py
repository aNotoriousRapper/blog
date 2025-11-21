import redis

from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

from . import extension
from . import cache
from . import utils


migrate = Migrate()  # 用于监听数据库中的结构是否改变以进行迁移
loginManager = LoginManager()
loginManager.login_view = "auth.Login"
loginManager.login_message = "请先进行登录！"

jwt = JWTManager()

from app.models import User

def CreateApp():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 开启跨域访问
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost"}})



    # 初始化redis
    extension.redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

    extension.db.init_app(app)
    migrate.init_app(app, extension.db)  # 将数据库连接对象传入
    loginManager.init_app(app)
    jwt.init_app(app)
    utils.limiter.init_app(app)

    # 开始redis定时任务
    cache.start_scheduler(app)

    @loginManager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 自定义登录拦截器
    # @loginManager.unauthorized_handler
    # def unauthorized_callback():
    #     if request.method == "POST":
    #         path = request.path
    #         if path.startswith('/post/') and path.endswith('/comments'):
    #             post_id = path.split('/')[2]
    #             next_url = f"/post/{post_id}"
    #         else:
    #             next_url = '/'
    #     else:
    #         next_url = request.path
    #     return redirect(url_for("auth.Login", next=next_url))

    from . import routes, auth, error_handler

    # 注册路由蓝图
    app.register_blueprint(routes.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(error_handler.bp)

    return app

