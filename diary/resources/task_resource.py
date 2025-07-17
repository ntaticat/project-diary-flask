from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from diary.extensions import db
from diary.models import Goal, Task
from diary.schemas import TaskSchema

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, required=True, help="Title is required")
parser.add_argument("completed", type=bool, default=False)
parser.add_argument("goal_id", type=int, required=True, help="Goal ID is required")


class TaskListResource(Resource):
  @swag_from("/diary/docs/tasks/get_all.yml")
  def get(self):
    tasks = Task.query.all()
    return tasks_schema.dump(tasks), 200

  @jwt_required()
  @swag_from("/diary/docs/tasks/post.yml")
  def post(self):
    args = parser.parse_args()

    goal_id = args["goal_id"]
    Goal.query.get_or_404(goal_id)

    current_user_id = get_jwt_identity()
    task = Task(
      title=args["title"],
      completed=args["completed"],
      goal_id=args["goal_id"],
      user_id=current_user_id,
    )
    db.session.add(task)
    db.session.commit()
    return task_schema.dump(task), 201


class TaskResource(Resource):
  @swag_from("/diary/docs/tasks/get_one.yml")
  def get(self, task_id):
    task = Task.query.get_or_404(task_id)
    return task_schema.dump(task)

  @jwt_required()
  @swag_from("/diary/docs/tasks/put.yml")
  def put(self, task_id):
    task = Task.query.get_or_404(task_id)
    current_user_id = get_jwt_identity()

    if task.goal.project.user_id != current_user_id and task.user_id != current_user_id:
      return {"message": "Forbidden"}, 403

    args = parser.parse_args()
    task.title = args["title"]
    task.completed = args["completed"]
    task.goal_id = args["goal_id"]
    db.session.commit()
    return task_schema.dump(task)

  @jwt_required()
  @swag_from("/diary/docs/tasks/delete.yml")
  def delete(self, task_id):
    task = Task.query.get_or_404(task_id)
    current_user_id = get_jwt_identity()

    if task.goal.project.user_id != current_user_id and task.user_id != current_user_id:
      return {"message": "Forbidden"}, 403

    db.session.delete(task)
    db.session.commit()
    return "", 204


class TaskByGoalResource(Resource):
  @swag_from("/diary/docs/tasks/get_by_goal.yml")
  def get(self, goal_id):
    goal = Goal.query.get_or_404(goal_id)
    tasks = Task.query.filter_by(goal_id=goal.id).all()
    return tasks_schema.dump(tasks)
