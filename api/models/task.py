from datetime import datetime
from api.models.db import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    project = db.Column(db.String(100))
    description = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def __repr__(self):
      return f"Ticket('{self.id}', '{self.name}'"

    def serialize(self):
      task = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      return task