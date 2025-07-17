from werkzeug.security import check_password_hash, generate_password_hash

from diary.extensions import db


class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password_hash = db.Column(db.String(256), nullable=False)

  projects = db.relationship("Project", backref="user", passive_deletes=True)
  favorite_projects = db.relationship(
    "FavoriteProject", back_populates="user", cascade="all, delete-orphan"
  )
  goals = db.relationship("Goal", backref="user", passive_deletes=True)
  tasks = db.relationship("Task", backref="user", passive_deletes=True)
  logs = db.relationship("Log", backref="user", passive_deletes=True)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)


class Project(db.Model):
  __tablename__ = "projects"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  description = db.Column(db.String(512))
  user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

  goals = db.relationship(
    "Goal", backref="project", cascade="all, delete-orphan", passive_deletes=True
  )
  favorited_by = db.relationship(
    "FavoriteProject", back_populates="project", cascade="all, delete-orphan"
  )


class FavoriteProject(db.Model):
  __tablename__ = "favorite_projects"

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  project_id = db.Column(
    db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
  )
  created_at = db.Column(db.DateTime, default=db.func.now())

  user = db.relationship("User", back_populates="favorite_projects")
  project = db.relationship("Project", back_populates="favorited_by")


class Goal(db.Model):
  __tablename__ = "goals"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  description = db.Column(db.String(255))
  status = db.Column(db.String(50), default="pending")
  approved = db.Column(db.Boolean, default=False)

  project_id = db.Column(
    db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
  )
  user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

  logs = db.relationship("Log", backref="goal", cascade="all, delete-orphan", passive_deletes=True)
  tasks = db.relationship(
    "Task", backref="goal", cascade="all, delete-orphan", passive_deletes=True
  )


class Log(db.Model):
  __tablename__ = "logs"
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, default=db.func.now())
  goal_id = db.Column(db.Integer, db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)


class Task(db.Model):
  __tablename__ = "tasks"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), nullable=False)
  completed = db.Column(db.Boolean, default=False)
  goal_id = db.Column(db.Integer, db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
