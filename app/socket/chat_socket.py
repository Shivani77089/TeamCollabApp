
# app/socket/chat_socket.py

from flask_socketio import disconnect, emit, join_room
from flask import request
import jwt
from app import socketio
from flask_jwt_extended import decode_token
from flask_socketio import disconnect


@socketio.on('connect')
def connect_handler(auth):
    token = auth.get('token') if auth else None
    if not token:
        print("Missing token")
        return disconnect()

    try:
        decoded = decode_token(token)
        user_identity = decoded['sub']
        print(f"Connected user: {user_identity}")
        # Optionally store user info in socket context (like flask.g)
    except Exception as e:
        print(f"Token decode failed: {e}")
        return disconnect()


@socketio.on("join")
def handle_join(data):
    user = request.environ.get('user')
    channel = data.get("channel_id")
    print(f"[JOIN] {user['email']} -> channel {channel}")
    join_room(channel)
    emit("receive_message", {"user": "System", "message": f"{user['name']} joined"}, room=channel)

