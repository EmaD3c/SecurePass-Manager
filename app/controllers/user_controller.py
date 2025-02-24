from flask import request, jsonify
from models.user import User
import jwt
from datetime import datetime, timedelta
from controllers.database_handler import DatabaseHandler

database_handler = DatabaseHandler(".db")

SECRET_KEY = 'your-secret-key'

def get_user_by_email(email):
    """Récupère un utilisateur par son email."""
    return database_handler.get_user_by_email(email)

def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    # Cree un nouvel utilisateur
    new_user = User(email=email, password=password)
    database_handler.save_user(new_user)  # database handler sauvegarde l'user

    token = jwt.encode({
        'user_id': new_user.id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({"token": token}), 201

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user.check_password(password):
        return jsonify({"error": "Invalid password"}), 401

    # Génère un token JWT
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({"token": token}), 200
