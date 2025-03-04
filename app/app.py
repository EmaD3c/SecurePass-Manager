from flask import Flask
from routes.auth import auth_bp
from controllers.database_handler import DatabaseHandler, DATABASE_URL
from database import db

# Crée les tables nécessaires dans la base de données
db.create_tables()

def create_app():
    app = Flask(__name__)

    # blueprint
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
