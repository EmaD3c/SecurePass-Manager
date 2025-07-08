import os
from flask import Flask
from routes.auth import auth_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from controllers.database_handler import Base, engine

def create_app():
    app = Flask(__name__)

    # Configuration of Flask-JWT-Extended
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback-secret')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']  # The tokens will be in the HTTP headers
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token validity period

    # Initialisation of JWTManager
    jwt = JWTManager(app)


    CORS(app)

    Base.metadata.create_all(engine)

    # blueprint
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
