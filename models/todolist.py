from app import login_manager, app, db, migrate
from flask_login import UserMixin
from sqlalchemy.schema import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from models.users import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class ListaDeTarefas(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300))
    usuario_id = db.Column(db.Integer(), db.ForeignKey('usuario.id'))
    usuario = db.relationship("Usuario", backref="listadetarefas")
    
    __table_args__ = (UniqueConstraint('titulo', 'usuario_id', name='unique_title_per_user'),)

    def __init__(self, titulo, descricao, usuario_id):
        self.titulo = titulo
        self.descricao = descricao
        self.usuario_id = usuario_id