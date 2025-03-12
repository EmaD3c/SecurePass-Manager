from flask import Blueprint, request, jsonify
from controllers.user_controller import register, login
from flask_jwt_extended import jwt_required
from controllers.password_controller import add_password, update_password, delete_password

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
    """ Ajouter un mot de passe """
    return add_password()

@auth_bp.route('/update_password', methods=['PUT'])
@jwt_required()
def update_password_route():
    """ Modifier un mot de passe """
    return update_password()

@auth_bp.route('/delete_password', methods=['DELETE'])
@jwt_required()
def delete_password_route():
    """ Supprimer un mot de passe """
    return delete_password()
