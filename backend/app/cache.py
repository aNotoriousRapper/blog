import functools
import json

from apscheduler.schedulers.background import BackgroundScheduler

from .extension import redis_client, db
from .models import Post
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)




def redis_cache(key_prefix="", ttl=300):
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            raw_key = f"{key_prefix}:{func.__name__}:{args}:{kwargs}"
            cache_key = raw_key.replace(" ", "")

            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            result = func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))

            return result

        def invalidate(*args, **kwargs):
            raw_key = f"{key_prefix}:{func.__name__}:{args}:{kwargs}"
            cache_key = raw_key.replace(" ", "")
            redis_client.delete(cache_key)

        wrapper.invalidate = invalidate

        return wrapper
    return decorator


def start_scheduler(app):
    logger.info("开始任务！！！")
    def sync_views_to_db():

        logger.info("执行任务！！！")
        with app.app_context():  # <- 关键
            # 获取所有增量 key
            keys = redis_client.keys("post:*:views")
            for key in keys:
                post_id = int(key.split(":")[1])

                delta_views = int(redis_client.hget(f"post:{post_id}:views", "delta") or 0)
                if delta_views == 0:
                    continue

                if delta_views > 0:
                    # 更新数据库
                    base_views = int(redis_client.hget("post:{}:views".format(post_id), "base") or 0)
                    post = Post.query.get(post_id)
                    post.views = base_views + delta_views
                    db.session.commit()



    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_views_to_db, 'interval', minutes=1)
    scheduler.start()