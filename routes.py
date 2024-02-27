from flask import request, jsonify, render_template
from app import app, db
from models import Usuario, ListaDeTarefas
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from schemas import *


bcrypt = Bcrypt(app)

#Rotas do Usuário   
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
    listas_do_usuario = ListaDeTarefas.query.filter_by(usuario_id=user_id).all()

    for i in listas_do_usuario:
        db.session.delete(i)

    usuario = Usuario.query.get(user_id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'msg': 'Usuário excluído com sucesso!'})





#Rotas da Lista de Tarefas
@app.route("/todolist", methods=['POST'])
@login_required
def add_todolist():
    user_id = current_user.id
    titulo = request.json["titulo"]  
    descricao = request.json.get("descricao")

    new_todolist = ListaDeTarefas(titulo, descricao, user_id)
    db.session.add(new_todolist)
    db.session.commit()

    return listadetarefa_schema.jsonify(new_todolist)

@app.route("/todolist/<id>", methods=['PUT'])
@login_required
def update_todolist(id):

    todolist = ListaDeTarefas.query.get(id)

    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para alterar esta tarefa!'})

    titulo = request.json.get("titulo")  
    descricao = request.json.get("descricao")

    todolist.titulo = titulo
    todolist.descricao = descricao
    
    db.session.commit()

    return listadetarefa_schema.jsonify(todolist)


@app.route("/todolist/<id>", methods=['DELETE'])
@login_required
def delete_todolist(id):

    todolist = ListaDeTarefas.query.get(id)

    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para excluir esta tarefa!'})
    
    tarefas_do_usuario = Tarefa.query.filter_by(lista_de_tarefas_id=id).all()
    for i in tarefas_do_usuario:
        db.session.delete(i)

    db.session.delete(todolist)
    db.session.commit()

    return jsonify({'msg': 'Lista de Tarefa excluída com sucesso!'})