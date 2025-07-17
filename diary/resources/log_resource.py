from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from diary.extensions import db
from diary.models import Goal, Log
from diary.schemas import LogSchema

log_schema = LogSchema()
logs_schema = LogSchema(many=True)

parser = reqparse.RequestParser()
parser.add_argument("content", type=str, required=True, help="Content is required")
parser.add_argument("goal_id", type=int, required=True, help="Goal ID is required")


class LogListResource(Resource):
  @swag_from("/diary/docs/logs/get_all.yml")
  def get(self):
    logs = Log.query.all()
    return logs_schema.dump(logs), 200

  @jwt_required()
  @swag_from("/diary/docs/logs/post.yml")
  def post(self):
    args = parser.parse_args()
    # validación de si existe el goal
    goal_id = args["goal_id"]
    Goal.query.get_or_404(goal_id)

    current_user_id = get_jwt_identity()
    log = Log(content=args["content"], goal_id=goal_id, user_id=current_user_id)
    db.session.add(log)
    db.session.commit()
    return log_schema.dump(log), 201


class LogResource(Resource):
  @swag_from("/diary/docs/logs/get_one.yml")
  def get(self, log_id):
    log = Log.query.get_or_404(log_id)
    return log_schema.dump(log)

  @jwt_required()
  @swag_from("/diary/docs/logs/put.yml")
  def put(self, log_id):
    log = Log.query.get_or_404(log_id)
    current_user_id = get_jwt_identity()

    if log.goal.project.user_id != current_user_id:
      return {"message": "Forbidden"}, 403

    args = parser.parse_args()
    log.content = args["content"]
    log.goal_id = args["goal_id"]
    db.session.commit()
    return log_schema.dump(log)

  @jwt_required()
  @swag_from("/diary/docs/logs/delete.yml")
  def delete(self, log_id):
    log = Log.query.get_or_404(log_id)
    current_user_id = get_jwt_identity()

    if log.goal.project.user_id != current_user_id and log.user_id != current_user_id:
      return {"message": "Forbidden"}, 403

    db.session.delete(log)
    db.session.commit()
    return "", 204


class LogByGoalResource(Resource):
  @swag_from("/diary/docs/logs/get_by_goal.yml")
  def get(self, goal_id):
    goal = Goal.query.get_or_404(goal_id)
    logs = Log.query.filter_by(goal_id=goal.id).all()
    return logs_schema.dump(logs)
