from config import db
from datetime import datetime

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_json(self):
        return {
            "uid": self.uid,
            "username": self.username,
            "created_at": self.created_at,
        }

class Ticket(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.uid"), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_json(self):
        return {
            "tid": self.tid,
            "title": self.title,
            "description": self.description,
            "owner_id": self.owner_id,
            "completed": self.completed,
            "created_at": self.created_at,
        }
    
