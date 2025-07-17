from flasgger import swag_from
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse

from diary.extensions import db
from diary.models import User
from diary.schemas import UserSchema

user_schema = UserSchema()

register_parser = reqparse.RequestParser()
register_parser.add_argument("username", type=str, required=True)
register_parser.add_argument("password", type=str, required=True)

login_parser = register_parser.copy()


class RegisterResource(Resource):
  @swag_from("/diary/docs/auth/register.yml")
  def post(self):
    data = register_parser.parse_args()
    if User.query.filter_by(username=data["username"]).first():
      return {"message": "Username already exists"}, 400

    user = User(username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201


class LoginResource(Resource):
  @swag_from("/diary/docs/auth/login.yml")
  def post(self):
    data = login_parser.parse_args()
    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
      return {"message": "Invalid credentials"}, 401

    token = create_access_token(
      identity=str(user.id), additional_claims={"username": user.username}
    )
    return {"access_token": token}, 200
