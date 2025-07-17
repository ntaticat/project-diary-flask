import os
import secrets


class BaseConfig:
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_hex(32))


class DevelopmentConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///db.sqlite3")
  DEBUG = True


class ProductionConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")  # No default
  DEBUG = False
