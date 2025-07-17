import sqlite3

from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Engine, event

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()


@event.listens_for(Engine, "connect")
def enable_foreign_keys(connection, _):
  if isinstance(connection, sqlite3.Connection):
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()
