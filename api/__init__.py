from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from api.models.db import db
from config import Config

# ============ Import Models ============
from api.models.user import User
from api.models.profile import Profile
from api.models.task import Task
from api.models.issue import Issue

# ============ Import Views ============
from api.views.auth import auth
from api.views.tasks import tasks
from api.views.issues import issues

cors = CORS()
migrate = Migrate() 
list = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE', 'LINK']

def create_app(config):
  app = Flask(__name__)
  app.config.from_object(config)

  db.init_app(app)
  migrate.init_app(app, db)
  cors.init_app(app, supports_credentials=True, methods=list)

  # ============ Register Blueprints ============
  app.register_blueprint(auth, url_prefix='/api/auth') 
  app.register_blueprint(tasks, url_prefix='/api/tasks')
  app.register_blueprint(issues, url_prefix='/api/issues')

  return app

app = create_app(Config)