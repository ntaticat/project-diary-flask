from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from diary.extensions import db
from diary.models import FavoriteProject, Project
from diary.schemas import FavoriteProjectSchema

favorite_schema = FavoriteProjectSchema()
favorites_schema = FavoriteProjectSchema(many=True)


class FavoriteProjectListResource(Resource):
  @swag_from("/diary/docs/favorite_projects/get_all.yml")
  @jwt_required()
  def get(self):
    user_id = get_jwt_identity()
    favorites = FavoriteProject.query.filter_by(user_id=user_id).all()
    return favorites_schema.dump(favorites)


class FavoriteProjectResource(Resource):
  @swag_from("/diary/docs/favorite_projects/post.yml")
  @jwt_required()
  def post(self, project_id):
    user_id = get_jwt_identity()

    # Check if the project exists
    Project.query.get_or_404(project_id)

    # Avoid duplicate favorites
    existing = FavoriteProject.query.filter_by(user_id=user_id, project_id=project_id).first()
    if existing:
      return {"message": "Already favorited"}, 400

    favorite = FavoriteProject(user_id=user_id, project_id=project_id)
    db.session.add(favorite)
    db.session.commit()
    return favorite_schema.dump(favorite), 201

  @swag_from("/diary/docs/favorite_projects/delete.yml")
  @jwt_required()
  def delete(self, project_id):
    current_user_id = get_jwt_identity()
    favorite = FavoriteProject.query.filter_by(
      user_id=current_user_id, project_id=project_id
    ).first_or_404()

    if favorite.user_id != current_user_id:
      return {"message": "Forbidden"}, 403

    db.session.delete(favorite)
    db.session.commit()
    return {"message": "Favorite removed"}, 204
