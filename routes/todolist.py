from flask import request, jsonify, render_template
from app import app, db, bcrypt

from models.users import Usuario
from models.todolist import ListaDeTarefas
from models.tasks import Tarefa

from schemas.users import UsuarioSchema, usuario_schema, usuarios_schema
from schemas.todolist import ListaDeTarefasSchema, listadetarefa_schema, listadetarefas_schema
from schemas.tasks import TarefaSchema, tarefa_schema, tarefas_schema

from flask_login import login_user, login_required, logout_user, current_user


#Rotas da Lista de Tarefas
@app.route("/todolist", methods=['GET'])
@login_required
def get_todolist():
    user_id = current_user.id
    all_todolist = ListaDeTarefas.query.filter_by(usuario_id=user_id).all()
    result = listadetarefas_schema.dump(all_todolist)
    return jsonify(result)

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

    if descricao is None:
        descricao = todolist.descricao
    
    if titulo is None:
        titulo = todolist.titulo

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
    
