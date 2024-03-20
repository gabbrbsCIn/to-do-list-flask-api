from app import login_manager, app, db, migrate
from flask_login import UserMixin
from sqlalchemy.schema import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from models.users import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Tarefa(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300))
    status = db.Column(db.String(10), nullable=False)
    prazo_final = db.Column(db.DateTime)
    prioridade = db.Column(db.Integer, nullable=False)
    lista_de_tarefas_id = db.Column(db.Integer(), db.ForeignKey('lista_de_tarefas.id'))
    lista_de_tarefas = db.relationship("ListaDeTarefas", backref="tarefa")

    def __init__(self, titulo, descricao, status, prazo_final, prioridade, lista_de_tarefas_id):
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.prazo_final = prazo_final
        self.prioridade = prioridade
        self.lista_de_tarefas_id = lista_de_tarefas_id