from .auth import auth_bp
from .team import team_bp
from .message import message_bp
from flask import Flask


def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(message_bp)

