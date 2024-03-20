from app import login_manager, app, db, migrate
from flask_login import UserMixin
from sqlalchemy.schema import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(300), unique=True, nullable=False)
    senha = db.Column(db.String(300), nullable=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha