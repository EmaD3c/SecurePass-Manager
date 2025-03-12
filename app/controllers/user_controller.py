from flask import request, jsonify
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from controllers.database_handler import db
from flask_jwt_extended import create_access_token


def get_user_by_email(email):
    return db.query(User).filter_by(email=email).first()

def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    print (email, password)

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    existing_user = get_user_by_email(email=email)

    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)

    # Crée un nouvel utilisateur
    new_user = User(email=email, password=hashed_password)
    save_user(email, hashed_password)

    # Crée un token JWT avec Flask-JWT-Extended
    token = create_access_token(identity=str(new_user.id))

    return jsonify({"token": token}), 201

def login():
    data = request.get_json()

    # Vérification des données d'entrée
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Recherche de l'utilisateur par email
    user = db.query(User).filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 401

    # Vérification du mot de passe
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid password"}), 401

     # Crée un token JWT avec Flask-JWT-Extended
    token = create_access_token(identity=str(user.id))

    return jsonify({"token": token}), 200

def save_user(email, password):
    user_to_save = User(
        email = email,
        password = password
    )

    db.add(user_to_save)
    db.commit()


def update_user(self, user):
    """
    Met à jour un utilisateur dans la base de données.
    """
    conn = self.connect()
    if conn is None:
        print("Failed to connect to the database. Cannot update user.")
        return None
    
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET email = %s, password = %s
        WHERE id = %s
    ''', (user.email, user.password, user.id))

    conn.commit()
    conn.close()

def delete_user(self, user_id):
    """
    Supprime un utilisateur de la base de données.
    """
    conn = self.connect()
    if conn is None:
        print("Failed to connect to the database. Cannot delete user.")
        return None
    
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM users WHERE id = %s
    ''', (user_id,))

    conn.commit()
    conn.close()
