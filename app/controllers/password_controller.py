from flask import jsonify, request
from models.password import Password
from werkzeug.security import generate_password_hash, check_password_hash
from controllers.database_handler import db_session
from flask_jwt_extended import get_jwt_identity


def add_password():

    user_id = get_jwt_identity() # Récupère l'identifiant de l'utilisateur
    data = request.get_json() # Récupère les données de la requête

    if not data or 'name' not in data or 'password' not in data:
        return jsonify({"error": "Name and password required"}), 400

    new_password = Password(name=data['name'], password=data['password'], user_id=user_id)

    db_session.add(new_password)
    db_session.commit()

    return jsonify({"message": "Password updated successfully"}), 201

def update_password(password_id):

    user_id = get_jwt_identity()
    data = request.get_json()

    password_entry = db_session.query(Password).filter_by(id=password_id, user_id=user_id).first()

    if not password_entry:
        return jsonify({"error": "Password not found"}), 404

    if 'password' in data:
        password_entry.password = data['password']

    db_session.commit()
    return jsonify({"message": "Password updated successfully"}), 200

def delete_password(password_id):

    user_id = get_jwt_identity()

    password_entry = db_session.query(Password).filter_by(id=password_id, user_id=user_id).first()

    if not password_entry:
        return jsonify({"error": "Password not found"}), 404

    db_session.delete(password_entry)
    db_session.commit()

    return jsonify({"message": "Password deleted"}), 200

def list_passwords():

    user_id = get_jwt_identity()

    passwords = db_session.query(Password).filter_by(user_id=user_id).all()

    return jsonify([password.to_dict() for password in passwords]), 200
