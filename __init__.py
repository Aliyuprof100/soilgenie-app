# soilgenie/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask import render_template
import datetime

load_dotenv()

# Initialize extensions WITHOUT an app instance first
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate() # <--- Initialize Migrate here

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    # MAKE SURE YOU HAVE THIS ENVIRONMENT VARIABLE SET ON RENDER
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///soilgenie.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Now, link the extensions to the created app instance
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db) # <--- Link it to the app AND the db instance here

    # Configure Flask-Login
    login_manager.login_view = 'main.index' # Redirect to landing page if not logged in
    login_manager.login_message_category = 'info'
    
    @app.context_processor
    def inject_current_year():
        """Injects the current year into all templates."""
        return {'current_year': datetime.datetime.now().year}

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    # Import and register blueprints
    from .auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback() # Rollback any broken db sessions
        return render_template('500.html'), 500

    return app