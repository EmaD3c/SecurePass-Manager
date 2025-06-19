from flask import request, jsonify
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from controllers.database_handler import db_session
from flask_jwt_extended import create_access_token


def get_user_by_email(email):
    return db_session.query(User).filter_by(email=email).first()

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
    print(hashed_password)

    # Create new user
    new_user = User(email=email, password=hashed_password)
    save_user(email, hashed_password)

    # Create a JWT token with Flask-JWT-Extended
    token = create_access_token(identity=str(new_user.id))

    return jsonify({"token": token}), 201

def login():
    data = request.get_json()

    # Checking input data
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # User search by email
    user = db_session.query(User).filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 401

    # Password verification
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid password"}), 401

     # Create a JWT token with Flask-JWT-Extended
    token = create_access_token(identity=str(user.id))

    return jsonify({"token": token}), 200

def save_user(email, password):
    user_to_save = User(
        email = email,
        password = password
    )

    db_session.add(user_to_save)
    db_session.commit()


def update_user(self, user):
    """
    Updates a user in the database.
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
    Deletes a user from the database.
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
