from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.task import Task

tasks = Blueprint('tasks', 'tasks')

@tasks.route('/', methods=["POST"])
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data["profile_id"] = profile["id"]
  task = Task(**data)
  db.session.add(task)
  db.session.commit()
  return jsonify(task.serialize()), 201

@tasks.route('/', methods=["GET"])
def index():
  tasks = Task.query.all()
  return jsonify([task.serialize() for task in tasks]), 200

@tasks.route('/<id>', methods=["GET"])
def show(id):
  task = Task.query.filter_by(id=id).first()
  task_data = task.serialize()
  return jsonify(cat=task_data), 200

@tasks.route('/<id>', methods=["PUT"]) 
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  task = Task.query.filter_by(id=id).first()

  if task.profile_id != profile["id"]:
    return 'Forbidden', 403

  for key in data:
    setattr(task, key, data[key])

  db.session.commit()
  return jsonify(task.serialize()), 200

@tasks.route('/<id>', methods=["DELETE"]) 
@login_required
def delete(id):
  profile = read_token(request)
  task = Task.query.filter_by(id=id).first()

  if task.profile_id != profile["id"]:
    return 'Forbidden', 403

  db.session.delete(task)
  db.session.commit()
  return jsonify(message="Success"), 200