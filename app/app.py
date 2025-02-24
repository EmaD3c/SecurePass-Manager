from flask import Flask
from app.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)

    # blueprint
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
