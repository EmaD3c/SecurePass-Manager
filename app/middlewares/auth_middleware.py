from flask import request, jsonify
import jwt

SECRET_KEY = 'your-secret-key'

def auth_middleware(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            token = token.split(' ')[1]  # Bearer <token>
        except IndexError:
            return jsonify({"error": "Token format is invalid"}), 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if 'user_id' not in payload:
                return jsonify({"error": "Invalid token payload"}), 401
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return func(*args, **kwargs)
    return wrapper
