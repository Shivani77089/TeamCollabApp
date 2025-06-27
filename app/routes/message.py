# app/routes/message.py

from flask import Blueprint, request, jsonify
from app import db
from app.models.message import Message
from flask_jwt_extended import jwt_required, get_jwt_identity

message_bp = Blueprint("message", __name__)


@message_bp.route("/channel/<int:channel_id>/message", methods=["POST"])
@jwt_required()
def send_message(channel_id):
    data = request.get_json()
    identity = get_jwt_identity()

    message = Message(
        user_id=identity["id"],
        channel_id=channel_id,
        content=data["content"]
    )
    db.session.add(message)
    db.session.commit()

    return jsonify({"message": "Message sent", "message_data": message.to_dict()}), 201


@message_bp.route("/channel/<int:channel_id>/showmessages", methods=["GET"])
@jwt_required()
def get_channel_messages(channel_id):
    messages = Message.query.filter_by(channel_id=channel_id).order_by(Message.timestamp).all()
    return jsonify([msg.to_dict() for msg in messages])


