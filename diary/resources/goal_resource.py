from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from diary.extensions import db
from diary.models import Goal, Project
from diary.schemas import GoalSchema

goal_schema = GoalSchema()
goals_schema = GoalSchema(many=True)

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True, help="Name is required")
parser.add_argument("description", type=str)
parser.add_argument("status", type=str)
parser.add_argument("project_id", type=int, required=True, help="Project ID is required")


class GoalListResource(Resource):
  @swag_from("/diary/docs/goals/get_all.yml")
  def get(self):
    goals = Goal.query.all()
    return goals_schema.dump(goals)

  @jwt_required()
  @swag_from("/diary/docs/goals/post.yml")
  def post(self):
    args = parser.parse_args()
    project_id = args["project_id"]

    project = Project.query.get_or_404(project_id)

    user_id = get_jwt_identity()
    is_owner = project.user_id == user_id
    approved = is_owner

    goal = Goal(
      name=args["name"],
      description=args.get("description"),
      status=args.get("status"),
      approved=approved,
      project_id=project_id,
      user_id=user_id,
    )
    db.session.add(goal)
    db.session.commit()
    return goal_schema.dump(goal), 201


class GoalResource(Resource):
  @swag_from("/diary/docs/goals/get_one.yml")
  def get(self, goal_id=None):
    goal = Goal.query.get_or_404(goal_id)
    return goal_schema.dump(goal)

  @jwt_required()
  @swag_from("/diary/docs/goals/put.yml")
  def put(self, goal_id):
    goal = Goal.query.get_or_404(goal_id)
    current_user_id = get_jwt_identity()

    # Si no accede dueño del proyecto o el creador del recurso
    if goal.user_id != current_user_id and goal.user_id != goal.project.user_id:
      return {"message": "Forbidden"}, 403

    # Si actualiza el creador del recurso
    if current_user_id == goal.user_id:
      goal.approved = False

    args = parser.parse_args()
    goal.name = args["name"]
    goal.description = args.get("description")
    goal.status = args.get("status")
    goal.project_id = args["project_id"]
    db.session.commit()
    return goal_schema.dump(goal)

  @jwt_required()
  @swag_from("/diary/docs/goals/delete.yml")
  def delete(self, goal_id):
    goal = Goal.query.get_or_404(goal_id)
    current_user_id = get_jwt_identity()

    if goal.project.user_id != current_user_id:
      return {"message": "Forbidden"}, 403

    db.session.delete(goal)
    db.session.commit()
    return "", 204


class GoalByProjectResource(Resource):
  @swag_from("/diary/docs/goals/get_by_project.yml")
  def get(self, project_id):
    project = Project.query.get_or_404(project_id)
    goals = Goal.query.filter_by(project_id=project.id).all()
    return goals_schema.dump(goals)
