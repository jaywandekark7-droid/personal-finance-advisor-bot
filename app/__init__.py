import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-change-this-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///finance.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .models import User
    from .auth import auth_bp
    from .main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()

    return app
