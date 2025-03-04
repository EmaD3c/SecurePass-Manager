from flask import Flask
from routes.auth import auth_bp
from controllers.database_handler import db

def create_app():
    app = Flask(__name__)

    # blueprint
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
