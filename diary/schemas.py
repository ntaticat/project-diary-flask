from diary.extensions import ma
from diary.models import FavoriteProject, Goal, Log, Project, Task, User


class UserSchema(ma.SQLAlchemySchema):
  class Meta:
    model = User
    load_instance = True


class ProjectSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Project
    include_fk = True
    load_instance = True


class FavoriteProjectSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = FavoriteProject
    load_instance = True

  id = ma.auto_field()
  user_id = ma.auto_field()
  project_id = ma.auto_field()
  created_at = ma.auto_field()


class GoalSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Goal
    include_fk = True
    load_instance = True


class LogSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Log
    include_fk = True
    load_instance = True


class TaskSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Task
    include_fk = True
    load_instance = True
