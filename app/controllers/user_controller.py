from flask import request, jsonify
from models.user import User
import jwt
from datetime import datetime, timedelta
from controllers.database_handler import DatabaseHandler
from werkzeug.security import check_password_hash

database_handler = DatabaseHandler(".db")

SECRET_KEY = 'your-secret-key'

from models import User

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()  # Cherche l'utilisateur par son email

def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    # Crée un nouvel utilisateur
    new_user = User(email=email, password=password)
    print(f"Before saving: {new_user.__dict__}")

    database_handler.save_user(new_user)  

    print(f"After saving: {new_user.__dict__}")

    token = jwt.encode({
        'user_id': new_user.id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({"token": token}), 201

def login():
    data = request.get_json()

    # Vérification des données d'entrée
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Recherche de l'utilisateur par email
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 401

    # Vérification du mot de passe
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid password"}), 401

    # Création du payload pour le JWT
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }

    # Création du token JWT
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return jsonify({"token": token}), 200
