from flask import Flask
from routes.auth import auth_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from controllers.database_handler import Base, engine

def create_app():
    app = Flask(__name__)

    # Configuration de Flask-JWT-Extended
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']  # Les tokens seront dans les en-têtes HTTP
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Durée de validité du token

    # Initialisation de JWTManager
    jwt = JWTManager(app)


    CORS(app)

    Base.metadata.create_all(engine)

    # blueprint
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
