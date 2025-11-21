from flask import Blueprint
from flask import render_template

bp = Blueprint("error_handler", __name__)

@bp.app_errorhandler(404)  # 如果你在蓝图中
def not_found_error(error):
    return render_template('404.html'), 404
