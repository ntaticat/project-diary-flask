import os

from flasgger import Swagger
from flask import Flask
from flask.cli import load_dotenv
from flask_restful import Api

from config import DevelopmentConfig, ProductionConfig
from diary.extensions import db, jwt, ma
from diary.resources.auth_resource import LoginResource, RegisterResource
from diary.resources.favorite_project_resource import (
  FavoriteProjectListResource,
  FavoriteProjectResource,
)
from diary.resources.goal_resource import GoalByProjectResource, GoalListResource, GoalResource
from diary.resources.log_resource import LogByGoalResource, LogListResource, LogResource
from diary.resources.project_resource import ProjectListResource, ProjectResource
from diary.resources.task_resource import TaskByGoalResource, TaskListResource, TaskResource

load_dotenv()


def create_app():
  app = Flask(__name__)
  config_class = ProductionConfig if os.getenv("FLASK_ENV") == "production" else DevelopmentConfig
  app.config.from_object(config_class)

  db.init_app(app)
  ma.init_app(app)
  jwt.init_app(app)

  api = Api(app)
  api.add_resource(RegisterResource, "/auth/register")
  api.add_resource(LoginResource, "/auth/login")
  api.add_resource(ProjectListResource, "/projects")
  api.add_resource(ProjectResource, "/projects/<int:project_id>")
  api.add_resource(GoalListResource, "/goals")
  api.add_resource(GoalResource, "/goals/<int:goal_id>")
  api.add_resource(GoalByProjectResource, "/projects/<int:project_id>/goals")
  api.add_resource(LogListResource, "/logs")
  api.add_resource(LogResource, "/logs/<int:log_id>")
  api.add_resource(LogByGoalResource, "/goals/<int:goal_id>/logs")
  api.add_resource(TaskListResource, "/tasks")
  api.add_resource(TaskResource, "/tasks/<int:task_id>")
  api.add_resource(TaskByGoalResource, "/goals/<int:goal_id>/tasks")
  api.add_resource(FavoriteProjectListResource, "/favorites")
  api.add_resource(FavoriteProjectResource, "/favorites/<int:project_id>")

  Swagger(
    app,
    template={
      "swagger": "2.0",
      "info": {
        "title": "Diary API",
        "description": "API for personal project diary",
        "version": "1.0.0",
      },
      "securityDefinitions": {
        "Bearer": {
          "type": "apiKey",
          "name": "Authorization",
          "in": "header",
          "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'",
        }
      },
      "security": [{"Bearer": []}],
      "definitions": {
        "User": {
          "type": "object",
          "properties": {
            "id": {"type": "integer", "example": 1},
            "username": {"type": "string", "example": "rafael"},
          },
        },
        "Project": {
          "type": "object",
          "properties": {
            "id": {"type": "integer", "example": 1},
            "name": {"type": "string", "example": "Cybersecurity"},
            "description": {
              "type": "string",
              "example": "Learning sysadmin tools",
            },
            "user_id": {"type": "integer", "example": 1},
          },
        },
        "FavoriteProject": {
          "type": "object",
          "properties": {
            "id": {"type": "integer", "example": 1},
            "user_id": {"type": "integer", "example": 3},
            "project_id": {"type": "integer", "example": 7},
            "created_at": {
              "type": "string",
              "format": "date-time",
              "example": "2025-06-19T13:45:30",
            },
          },
        },
        "Goal": {
          "type": "object",
          "properties": {
            "id": {"type": "integer", "example": 1},
            "name": {"type": "string", "example": "Learn Docker"},
            "description": {
              "type": "string",
              "example": "Complete Docker tutorial",
            },
            "status": {"type": "string", "example": "in_progress"},
            "approved": {"type": "boolean", "example": True},
            "project_id": {"type": "integer", "example": 1},
            "user_id": {"type": "integer", "example": 1},
          },
        },
        "Task": {
          "type": "object",
          "properties": {
            "id": {"type": "integer", "example": 5},
            "title": {"type": "string", "example": "Read Flask-Restful docs"},
            "completed": {"type": "boolean", "example": False},
            "goal_id": {"type": "integer", "example": 1},
            "user_id": {"type": "integer", "example": 1},
          },
        },
        "Log": {
          "type": "object",
          "properties": {
            "id": {"type": "integer", "example": 3},
            "content": {
              "type": "string",
              "example": "Reviewed serialization strategies using Marshmallow",
            },
            "created_at": {
              "type": "string",
              "format": "date-time",
              "example": "2025-06-19T15:00:00Z",
            },
            "goal_id": {"type": "integer", "example": 1},
            "user_id": {"type": "integer", "example": 1},
          },
        },
      },
    },
  )

  return app
