from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy.schema import UniqueConstraint

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

class Tarefa(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300))
    status = db.Column(db.String(10), nullable=False)
    prazo_final = db.Column(db.DateTime)
    prioridade = db.Column(db.Integer, nullable=False)
    lista_de_tarefas_id = db.Column(db.Integer(), db.ForeignKey('lista_de_tarefas.id'))
    lista_de_tarefas = db.relationship("ListaDeTarefas", backref="tarefa")

    def __init__(self, titulo, descricao, status, prazo_final, prioridade):
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.prazo_final = prazo_final
        self.prioridade = prioridade


