from flask import Blueprint, request, jsonify
from controllers.user_controller import register, login
from flask_jwt_extended import jwt_required
from controllers.password_controller import add_password, update_password, delete_password, list_passwords

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_route():
    return register()

@auth_bp.route('/login', methods=['POST'])
def login_route():
    return login()

@auth_bp.route('/add_password', methods=['POST'])
@jwt_required()
def add_password_route():
    return add_password()

@auth_bp.route('/update_password', methods=['PUT'])
@jwt_required()
def update_password_route():
    return update_password()

@auth_bp.route('/delete_password', methods=['DELETE'])
@jwt_required()
def delete_password_route():
    return delete_password()

@auth_bp.route('/list_passwords', methods=['GET'])
@jwt_required()
def list_passwords_route():
    return list_passwords()
