import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from dotenv import load_dotenv
from flask_migrate import Migrate


load_dotenv()

app = Flask(__name__)

secret_key = os.environ.get("SECRET_KEY")



app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres.egnmntyafgtdjwdhmtbz:Tz8a4oIdPcPArvuO@aws-0-sa-east-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["SECRET_KEY"] = secret_key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app,db)



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
    titulo = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.String(300))
    usuario_id = db.Column(db.Integer(), db.ForeignKey('usuario.id'))
    usuario = db.relationship("Usuario", backref="listadetarefas")
    

    def __init__(self, titulo, descricao):
        self.titulo = titulo
        self.descricao = descricao

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


class UsuarioSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'nome', 'email', 'senha')


class ListaDeTarefasSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'titulo', 'descricao')

class TarefaSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'titulo', 'descricao', 'status', 'prazo_final', 'prioridade')

tarefa_schema = TarefaSchema()
tarefas_schema = TarefaSchema(many=True)

listadetarefa_schema = ListaDeTarefasSchema()
listadetarefas_schema = ListaDeTarefasSchema(many=True)

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)


# with app.app_context():
#     db.create_all()

@app.route('/users', methods=['POST'])
def add_user():
    nome = request.json['nome']
    email = request.json['email']
    senha = request.json['senha']

    hashed_password = bcrypt.generate_password_hash(senha).decode('utf8')
    new_user = Usuario(nome,email,hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return usuario_schema.jsonify(new_user)


@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    senha = request.json['senha']

    user = Usuario.query.filter_by(email=email).first()
    
    if user:
        if bcrypt.check_password_hash(user.senha, senha):
            login_user(user)
            return jsonify({'msg':'logado com sucesso!'})
    return jsonify({'erro': 'Usuário não encontrado'})

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'msg': 'Usuário deslogado!'})




@app.route('/users', methods=['GET'])
def get_users():

    all_users=Usuario.query.with_entities(Usuario.nome, Usuario.email).all()
    result = usuarios_schema.dump(all_users)

    return jsonify(result)

@app.route('/users', methods=['PUT'])
@login_required
def update_users():
    user_id = current_user.id
    usuario = Usuario.query.get(user_id)
    
    nome = request.json['nome']
    email = request.json['email']

    usuario.nome = nome
    usuario.email = email

    db.session.commit()

    return usuario_schema.jsonify(usuario)

@app.route("/users", methods=['DELETE'])
@login_required
def delete_users():
    user_id = current_user.id
    usuario = Usuario.query.get(user_id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'msg': 'Usuário excluído com sucesso!'})

    

if __name__ == '__main__':
    app.run(debug=True)