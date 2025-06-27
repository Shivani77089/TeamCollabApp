# app/models/team.py

from app import db
from datetime import datetime


class Team(db.Model):
    __tablename__ = "Teams"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Channel(db.Model):
    __tablename__ = "Channels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('Teams.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserTeam(db.Model):
    __tablename__ = "UserTeams"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('MyUser.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('Teams.id'))


class UserChannel(db.Model):
    __tablename__ = "UserChannels"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('MyUser.id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('Channels.id'))


