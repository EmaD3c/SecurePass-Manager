from flask import Flask
from routes.auth import auth_bp
from controllers.database_handler import DatabaseHandler

# Initialise le DatabaseHandler avec l'URL de la base de données
database_handler = DatabaseHandler("postgresql://postgres:postgres@db:5432/postgres")

# Crée les tables nécessaires dans la base de données
database_handler.create_tables()

def create_app():
    app = Flask(__name__)

    # blueprint
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
