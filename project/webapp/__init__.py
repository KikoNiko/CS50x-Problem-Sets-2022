from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


#configure database
db = SQLAlchemy()
DB_NAME = "database.db"

#define the application
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "cs50r0x!"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)

    from .main import main
    from .auth import auth

    app.register_blueprint(main, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    create_db(app)

    #Login manager stuff
    login_manager = LoginManager()
    #If not logged in redirect to login page
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

# Create database
def create_db(app):
    if not path.exists("webapp/" + DB_NAME):

        with app.app_context():
            db.create_all()
            
        return app

        