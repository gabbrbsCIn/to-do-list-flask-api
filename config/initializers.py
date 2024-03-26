from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate



def init_app(app):
    db = SQLAlchemy(app)
    ma = Marshmallow(app)
    migrate = Migrate(app, db)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    return [db, ma, migrate, bcrypt, login_manager] 
