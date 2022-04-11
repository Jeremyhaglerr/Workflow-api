from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.issue import Issue

issues = Blueprint('issues', 'issues')

@issues.route('/', methods=["POST"]) 
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data["profile_id"] = profile["id"]

  issue = Issue(**data)
  db.session.add(issue)
  db.session.commit()
  return jsonify(issue.serialize()), 201

@issues.route('/', methods=["GET"])
def index():
  issues = Issue.query.all()
  return jsonify([issue.serialize() for issue in issues]), 201

@issues.route('/<id>', methods=["GET"])
def show(id):
  issue = Issue.query.filter_by(id=id).first()
  return jsonify(issue.serialize()), 200

@issues.route('/<id>', methods=["PUT"]) 
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  issue = Issue.query.filter_by(id=id).first()

  if issue.profile_id != profile["id"]:
    return 'Forbidden', 403

  for key in data:
    setattr(issue, key, data[key])

  db.session.commit()
  return jsonify(issue.serialize()), 200