import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database():
    # 首先连接到默认的postgres数据库
    conn = psycopg2.connect(
        host='blog',
        user='postgres',
        password='zhuang20021118'  # 替换为你的postgres密码
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    # 创建数据库
    try:
        cursor.execute("CREATE DATABASE blog;")
        print("数据库 blog_db 创建成功")
    except psycopg2.Error as e:
        print(f"数据库可能已存在: {e}")

    # 创建用户
    try:
        cursor.execute("CREATE USER postgres WITH PASSWORD 'blog_password';")
        print("用户 postgres 创建成功")
    except psycopg2.Error as e:
        print(f"用户可能已存在: {e}")

    # 授予权限
    try:
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE blog TO postgres;")
        print("权限授予成功")
    except psycopg2.Error as e:
        print(f"权限授予失败: {e}")

    cursor.close()
    conn.close()


if __name__ == '__main__':
    create_database()