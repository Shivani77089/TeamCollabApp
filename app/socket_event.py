from flask_socketio import emit, join_room, leave_room, disconnect
from flask_jwt_extended import decode_token
from jwt.exceptions import ExpiredSignatureError
from datetime import datetime
# from urllib import request
from flask import request
from app import socketio, db
from app.models.message import Message
from app.models.user import User

from collections import defaultdict

# channel_id -> set of user emails
online_users = defaultdict(set)


@socketio.on("send_message")
def handle_send_message(data):
    token = data.get("token")
    message = data.get("message")
    channel_id = data.get("channel_id")

    if not token or not message or not channel_id:
        return

    try:
        decoded = decode_token(token)
    except ExpiredSignatureError:
        emit("error", {"message": "Token has expired. Please log in again."})
        disconnect()
        return
    except Exception as e:
        print(f"[{datetime.now()}] Token error: {e}")
        disconnect()
        return

    email = decoded["sub"]["email"]
    user = User.query.filter_by(email=email).first()

    if not user:
        emit("error", {"message": "User not found."})
        return

    # Update last_seen
    user.last_seen = datetime.utcnow()

    new_message = Message(
        user_id=user.id,
        channel_id=channel_id,
        content=message
    )
    db.session.add(new_message)
    db.session.commit()

    print(f"[{datetime.now()}] Message from {email} in channel {channel_id}: {message}")

    emit("receive_message", {
        "user": email,
        "message": message,
        "timestamp": new_message.timestamp.isoformat()
    }, room=channel_id)


@socketio.on("join")
def handle_join(data):
    token = data.get("token")
    channel_id = data.get("channel_id")

    if not token or not channel_id:
        return

    try:
        decoded = decode_token(token)
        email = decoded["sub"]["email"]
    except Exception as e:
        print(f"[{datetime.now()}] Token error during join: {e}")
        return

    user = User.query.filter_by(email=email).first()
    if user:
        user.last_seen = datetime.utcnow()
        db.session.commit()

    join_room(channel_id)
    online_users[channel_id].add(email)

    print(f"[{datetime.now()}] {email} joined room {channel_id}")

    emit("user_joined", {"email": email}, room=channel_id)
    emit("online_users", list(online_users[channel_id]), room=channel_id)


@socketio.on("leave")
def handle_leave(data):
    token = data.get("token")
    channel_id = data.get("channel_id")

    if not token or not channel_id:
        return

    try:
        decoded = decode_token(token)
        email = decoded["sub"]["email"]
    except Exception as e:
        print(f"[{datetime.now()}] Token error during leave: {e}")
        return

    user = User.query.filter_by(email=email).first()
    if user:
        user.last_seen = datetime.utcnow()
        db.session.commit()

    leave_room(channel_id)
    online_users[channel_id].discard(email)

    print(f"[{datetime.now()}] {email} left room {channel_id}")

    emit("user_left", {"email": email}, room=channel_id)
    emit("online_users", list(online_users[channel_id]), room=channel_id)


@socketio.on("get_history")
def handle_get_history(data):
    token = data.get("token")
    channel_id = data.get("channel_id")
    if not token or not channel_id:
        return

    try:
        decoded = decode_token(token)
    except ExpiredSignatureError:
        emit("error", {"message": "Token has expired. Please log in again."})
        disconnect()
        return
    except Exception as e:
        print(f"[{datetime.now()}] Token error: {e}")
        disconnect()
        return

    email = decoded["sub"]["email"]
    user = User.query.filter_by(email=email).first()

    if not user:
        emit("error", {"message": "User not found."})
        return

    # Update last_seen
    user.last_seen = datetime.utcnow()
    db.session.commit()

    messages = (
        Message.query
        .filter_by(channel_id=channel_id)
        .order_by(Message.timestamp.asc())
        .limit(50)
        .all()
    )

    history = [
        {
            "user": User.query.get(msg.user_id).email,
            "message": msg.content,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in messages
    ]

    emit("chat_history", history)


@socketio.on('logout')
def handle_logout():
    token = request.args.get('token')  # or from the client data
    if token:
        # Decode token, remove user from online list, etc.
        decoded = decode_token(token)
        email = decoded['sub']['email']
        # Remove user from any online rooms, sets, etc.
        for room_id, users in online_users.items():
            if email in users:
                users.remove(email)
                leave_room(room_id)
                emit('user_left', {'email': email}, room=room_id)
        print(f"{email} logged out.")


@socketio.on('join_channel')
def handle_join_channel(data):
    channel_name = data.get('channel_name')
    email = data.get('email')
    room = f"channel_{channel_name}"
    join_room(room)
    emit('system_message', {'msg': f'{email} joined {channel_name}'}, room=room)


@socketio.on('send_channel_message')
def handle_send_channel_message(data):
    channel_name = data.get('channel_name')
    message = data.get('message')
    sender = data.get('email')
    room = f"channel_{channel_name}"
    emit('receive_message', {'email': sender, 'msg': message}, room=room)
