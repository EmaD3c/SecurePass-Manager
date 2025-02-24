from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes.auth import auth_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # Initialise la base de données
    db.init_app(app)

    # Enregistre les Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app