from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres.egnmntyafgtdjwdhmtbz:Tz8a4oIdPcPArvuO@aws-0-sa-east-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy()
ma = Marshmallow(app)
db.init_app(app)


class Usuario(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(300), unique=True)

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email
        
class ListaDeTarefas(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300), nullable=False)
    usuario_id = db.Column(db.Integer(), db.ForeignKey('usuario.id'))
    usuario = db.relationship("Usuario", backref="listadetarefas")
    

    def __init__(self, titulo, descricao):
        self.titulo = titulo
        self.descricao = descricao

class Tarefa(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    prazo_final = db.Column(db.DateTime, nullable=True)
    prioridade = db.Column(db.Integer, nullable=False)
    lista_de_tarefas_id = db.Column(db.Integer(), db.ForeignKey('lista_de_tarefas.id'))
    lista_de_tarefas = db.relationship("ListaDeTarefas", backref="tarefa")

    def __init__(self, titulo, descricao, status, prazo_final, prioridade):
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.prazo_final = prazo_final
        self.prioridade = prioridade


class UsuarioSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'nome', 'email')



class ListaDeTarefasSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'titulo', 'descricao')

class TarefaSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'titulo', 'descricao', 'status', 'prazo_final', 'prioridade')

with app.app_context():
    db.create_all()




if __name__ == '__main__':
    app.run(debug=True)