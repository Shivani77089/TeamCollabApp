# app/routes/team.py

from flask import Blueprint, request, jsonify
from app import db
from app.models.team import Team, Channel, UserTeam, UserChannel
from flask_jwt_extended import jwt_required, get_jwt_identity

team_bp = Blueprint("team", __name__)


@team_bp.route("/team/create", methods=["POST"])
@jwt_required()
def create_team():
    data = request.get_json()
    identity = get_jwt_identity()
    team = Team(name=data["name"])
    db.session.add(team)
    db.session.commit()

    db.session.add(UserTeam(user_id=identity["id"], team_id=team.id))
    db.session.commit()

    return jsonify({"message": "Team created", "team_id": team.id}), 201


@team_bp.route("/team/<int:team_id>/join", methods=["POST"])
@jwt_required()
def join_team(team_id):
    identity = get_jwt_identity()
    link = UserTeam(user_id=identity["id"], team_id=team_id)
    db.session.add(link)
    db.session.commit()
    return jsonify({"message": "Joined team"}), 200


@team_bp.route("/channel/create", methods=["POST"])
@jwt_required()
def create_channel():
    data = request.get_json()
    channel = Channel(name=data["name"], team_id=data["team_id"])
    db.session.add(channel)
    db.session.commit()
    return jsonify({"message": "Channel created", "channel_id": channel.id}), 201


#
# @team_bp.route("/api/my_channels", methods=["GET"])
# @jwt_required()
# def get_user_channels():
#     user_data = get_jwt_identity()   # This is a dict: {'id': ..., 'email': ...}
#     user_id = user_data['id']
#
#     teams = db.session.query(Team).join(UserTeam).filter(UserTeam.user_id == user_id).all()
#
#     output = []
#     for team in teams:
#         channels = Channel.query.filter_by(team_id=team.id).join(UserChannel).filter(UserChannel.user_id == user_id).all()
#         output.append({
#             "team": team.name,
#             "channels": [ch.name for ch in channels]
#         })
#
#     return jsonify(output), 200
