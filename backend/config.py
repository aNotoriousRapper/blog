import os
from datetime import timedelta


class Config:
    # token
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or 'chigganeednogun'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # PostgreSQL 配置
    DB_USER = os.environ.get('DB_USER') or 'postgres'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'zhuang20021118'
    DB_HOST = os.environ.get('DB_HOST') or 'postgres_db'
    DB_PORT = os.environ.get('DB_PORT') or '5432'
    DB_NAME = os.environ.get('DB_NAME') or 'blog'

    # redis
    REDIS_HOST = os.environ.get('REDIS_HOST') or 'redis'
    REDIS_PORT = os.environ.get('REDIS_PORT') or '6379'

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'