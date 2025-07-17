from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from diary.extensions import db
from diary.models import Project
from diary.schemas import ProjectSchema

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True, help="Name is required")
parser.add_argument("description", type=str)


class ProjectListResource(Resource):
  @swag_from("/diary/docs/projects/get_all.yml")
  def get(self):
    projects = Project.query.all()
    return projects_schema.dump(projects)

  @jwt_required()
  @swag_from("/diary/docs/projects/post.yml")
  def post(self):
    args = parser.parse_args()
    current_user_id = get_jwt_identity()
    project = Project(
      name=args["name"], description=args.get("description"), user_id=current_user_id
    )
    db.session.add(project)
    db.session.commit()
    return project_schema.dump(project), 201


class ProjectResource(Resource):
  @swag_from("/diary/docs/projects/get_one.yml")
  def get(self, project_id=None):
    project = Project.query.get_or_404(project_id)
    return project_schema.dump(project)

  @swag_from("/diary/docs/projects/put.yml")
  @jwt_required()
  def put(self, project_id):
    project = Project.query.get_or_404(project_id)
    current_user_id = get_jwt_identity()

    if project.user_id != current_user_id:
      return {"message": "Forbidden"}, 403

    args = parser.parse_args()
    project.name = args["name"]
    project.description = args.get("description")
    db.session.commit()
    return project_schema.dump(project)

  @swag_from("/diary/docs/projects/delete.yml")
  @jwt_required()
  def delete(self, project_id):
    project = Project.query.get_or_404(project_id)
    current_user_id = get_jwt_identity()

    if project.user_id != current_user_id:
      return {"message": "Forbidden"}, 403

    db.session.delete(project)
    db.session.commit()
    return "", 204
