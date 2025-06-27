# app/models/message.py

from app import db
from datetime import datetime


class Message(db.Model):
    __tablename__ = "Messages"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("MyUser.id"))
    channel_id = db.Column(db.Integer, db.ForeignKey("Channels.id"))
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "channel_id": self.channel_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }
