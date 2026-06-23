from flask import Flask
from flask_login import LoginManager

from app.config import Config
from app.models import db
from app.models.user import User
from app.routes.auth_routes import auth_bp
from app.routes.booking_routes import booking_bp
from flask_talisman import Talisman



login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    Talisman(app)



def create_app():
    app = Flask(__name__)

    app.register_blueprint(booking_bp)

    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)

    app.register_blueprint(auth_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def home():
        return "Bienvenue sur Ticket Booking"
    
    print(app.url_map)

    return app