from app import CreateApp
from app import extension


app = CreateApp()

# 创建数据库相关内容
with app.app_context():
    extension.db.create_all()

if __name__ == '__main__':
    app.run(debug=True)