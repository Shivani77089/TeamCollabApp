# app/routes/auth.py

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from app import db
from app.models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "User already exists"}), 409

    user = User(email=data['email'], name=data['name'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user and check_password_hash(user.password_hash, data["password"]):
        access_token = create_access_token(identity={"id": user.id, "email": user.email})
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Invalid credentials"}), 401


@auth_bp.route("/")
def home():
    return redirect(url_for("auth.login_page"))


@auth_bp.route("/login-page")
def login_page():
    return render_template("login.html")


@auth_bp.route("/chat")
def chat_page():
    return render_template("chat.html")
