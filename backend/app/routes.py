import logging

from flask import Blueprint, url_for, redirect, jsonify, request
from flask import render_template
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from .models import Post, Tag, Comment, User
from .extension import db
from .cache import redis_cache
from .extension import redis_client
from .utils import limiter

bp = Blueprint("routes", __name__)

# 首页
@bp.route('/posts')
def GetPosts():
    # 查找帖子 todo 分页
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    posts = pagination.items

    return jsonify({
        "posts": [
            {
                "id": p.id,
                "title": p.title,
                "content": p.content,
                "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "author": p.author.username,
            }
            for p in posts
        ],
        "total": pagination.total,
        "page": page,
        "per_page": per_page,
        "pages": pagination.pages,
        "has_next": pagination.has_next
    }), 200

# 帖子内容
@bp.route('/post/<int:post_id>')
def PostPage(post_id):
    post = Post.query.get_or_404(post_id)

    # redis计数
    redis_client.hincrby(f"post:{post_id}:views", "delta", 1)

    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()
    post_details = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "views": post.views,
        "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "author": post.author.username,
        "comments": [
            {
                "id": comment.id,
                "content": comment.content,
                "username":  User.query.filter_by(id=comment.user_id).first().username,
                "user_id": comment.user_id,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for comment in comments
        ],
        "tags": [tag.name for tag in post.tags]
    }
    return jsonify(post_details), 200

# 发布帖子
@bp.route("/create", methods=["POST"])
@jwt_required()
def CreatePost():
    # 获取请求 body 数据
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    lTagName = data.get("tags", [])
    post = Post(title=title, content=content, user_id=int(get_jwt_identity()))

    lTag = []
    for sTagName in lTagName:
        tag = Tag.query.filter_by(name=sTagName).first()
        if not tag:
            tag = Tag(name=sTagName)
            db.session.add(tag)
        lTag.append(tag)

    # 绑定帖子和标签
    post.tags = lTag
    db.session.add(post)
    db.session.commit()
    return jsonify({"success": True, "message": "Successfully Published!"}), 200


# 发表评论到某帖子
@bp.route("/post/<int:post_id>/comments", methods=["POST"])
@jwt_required()
@limiter.limit("3/minute")
def PostComments(post_id):
    data = request.json
    logger = logging.getLogger("flask")
    logger.info(data)
    newComment = data.get("newComment")

    user_id = int(get_jwt_identity())
    if user_id:
        comment = Comment(content=newComment,
                          user_id=user_id,
                          post_id=post_id)
        db.session.add(comment)
        db.session.commit()
    return jsonify({"success": True, "message": "评论发布成功!"}), 200


# 删除评论
@bp.route("/comment/<int:comment_id>/delete", methods=["GET", "POST"])
def DeleteComment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)  # 删除单个对象
    db.session.commit()
    return redirect(url_for("routes.PostPage", post_id=comment.post_id))

@bp.route("/about")
def About():
    return render_template("about.html")

# 获取前十浏览量的帖子
@bp.route("/posts/rank")
def PostRank():
    posts_data = GetPostRank()
    for post_dict in posts_data:
        base_views = int(redis_client.hget("post:{}:views".format(post_dict["id"]), "base") or 0)
        delta_views = int(redis_client.hget("post:{}:views".format(post_dict["id"]), "delta") or 0)
        total_views = base_views + delta_views
        if total_views: post_dict["views"] = total_views
    return jsonify(posts_data), 200

@redis_cache("top_posts", ttl=300)
def GetPostRank():
    posts = Post.query.order_by(Post.views.desc()).all()
    top_posts = posts[0:10]
    posts_data = []
    for post in top_posts:
        dPost = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "views": post.views,
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "author": post.author.username,
        }
        posts_data.append(dPost)

        key = f"post:{post.id}:views"
        # 哈希结构写入 base 和 delta
        redis_client.hset(key, mapping={
            "base": post.views,
            "delta": 0
        })
        # 永不过期
        redis_client.persist(key)

    return posts_data


# todo 要迁移到auth里面
@bp.route("/api/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_access = create_access_token(identity=user_id)
    new_refresh = create_refresh_token(identity=user_id)
    return {
        "access_token": new_access,
        "refresh_token": new_refresh
    }