import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configure the app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soilgenie.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Link extensions to the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Configure Flask-Login
    login_manager.login_view = 'main.index' # Redirect to landing page if not logged in
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    # Import and register blueprints
    from .auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app