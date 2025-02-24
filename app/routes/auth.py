from flask import Blueprint, request, jsonify
from controllers.user_controller import register, login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_route():
    return register()

@auth_bp.route('/login', methods=['POST'])
def login_route():
    return login()
