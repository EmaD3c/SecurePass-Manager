from flask import jsonify, request
from models.password import Password
from controllers.database_handler import db_session
from flask_jwt_extended import get_jwt_identity
from utils.crypto import encrypt_password, decrypt_password
from cryptography.fernet import InvalidToken



def add_password():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'name' not in data or 'password' not in data:
        return jsonify({"error": "Name and password required"}), 400

    encrypted_pw = encrypt_password(data['password'])

    new_password = Password(name=data['name'], password=encrypted_pw, user_id=user_id)

    db_session.add(new_password)
    db_session.commit()

    return jsonify({"message": "Password added successfully"}), 201


def update_password(password_id):

    user_id = get_jwt_identity()
    data = request.get_json()

    password_entry = db_session.query(Password).filter_by(id=password_id, user_id=user_id).first()

    if not password_entry:
        return jsonify({"error": "Password not found"}), 404

    if 'password' in data:
        password_entry.password = encrypt_password(data['password'])

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

    result = []
    for p in passwords:
        try:
            decrypted_pw = decrypt_password(p.password)
        except InvalidToken:
            decrypted_pw = "[Mot de passe non lisible]"
        result.append({
            "id": p.id,
            "name": p.name,
            "password": decrypted_pw
        })

    return jsonify(result), 200

