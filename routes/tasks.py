from flask import request, jsonify, render_template
from app import app, db, bcrypt

from models.users import Usuario
from models.todolist import ListaDeTarefas
from models.tasks import Tarefa

from schemas.users import UsuarioSchema, usuario_schema, usuarios_schema
from schemas.todolist import ListaDeTarefasSchema, listadetarefa_schema, listadetarefas_schema
from schemas.tasks import TarefaSchema, tarefa_schema, tarefas_schema

from flask_login import login_user, login_required, logout_user, current_user

from utils.checkPermission import check_permission
from utils.getTaskById import get_task_by_id
from utils.getTasksByStatus import get_tasks_by_status


# Rotas da Tarefa
@app.route("/todolist/<id>/task", methods=['POST'])
@login_required
def add_task(id):
    todolist = ListaDeTarefas.query.get(id)
    error = check_permission(todolist)
    if error:
        return error

    titulo = request.json["titulo"]
    descricao = request.json.get("descricao")
    status = "A fazer"
    prazo_final = request.json.get("prazo_final")
    prioridade = request.json.get("prioridade")
    if prioridade is None:
        prioridade = 4

    new_task = Tarefa(titulo, descricao, status, prazo_final, prioridade, id)
    db.session.add(new_task)
    db.session.commit()

    return tarefa_schema.jsonify(new_task)

@app.route("/todolist/<id>/task/<id_task>/doing", methods=['PUT'])
@login_required
def update_status_task_doing(id, id_task):
    todolist = ListaDeTarefas.query.get(id)
    error = check_permission(todolist)
    if error:
        return error

    task = get_task_by_id(id_task)
    if task.lista_de_tarefas_id != int(id):
        return jsonify({'erro': 'Tarefa não encontrada nesta lista!'})

    task.status = "Fazendo"
    db.session.commit()
    return tarefa_schema.jsonify(task)

@app.route("/todolist/<id>/task/<id_task>/done", methods=['PUT'])
@login_required
def update_status_task_done(id, id_task):
    todolist = ListaDeTarefas.query.get(id)
    error = check_permission(todolist)
    if error:
        return error

    task = get_task_by_id(id_task)
    if task.lista_de_tarefas_id != int(id):
        return jsonify({'erro': 'Tarefa não encontrada nesta lista!'})

    task.status = "Concluída"
    db.session.commit()
    return tarefa_schema.jsonify(task)

@app.route("/todolist/<id>/task/<id_task>", methods=['PUT'])
@login_required
def update_task_priority(id, id_task):
    todolist = ListaDeTarefas.query.get(id)
    error = check_permission(todolist)
    if error:
        return error

    task = get_task_by_id(id_task)
    if task.lista_de_tarefas_id != int(id):
        return jsonify({'erro': 'Tarefa não encontrada nesta lista!'})

    prioridade = request.json.get("prioridade")
    if prioridade is None:
        prioridade = task.prioridade

    if not isinstance(prioridade, int):
        return jsonify({'erro': 'Prioridade inválida! Deve ser um número inteiro!'})

    if prioridade < 1 or prioridade > 5:
        return jsonify({'erro': 'Prioridade inválida! Deve ser um número de 1 a 4!'})

    task.prioridade = prioridade

    db.session.commit()
    return tarefa_schema.jsonify(task)

@app.route("/todolist/<id>/task", methods=['GET'])
@login_required
def get_tasks(id):
    todolist = ListaDeTarefas.query.get(id)
    error = check_permission(todolist)
    if error:
        return error

    all_tasks = Tarefa.query.filter_by(lista_de_tarefas_id=id).all()

    if not all_tasks:
        return jsonify({'msg': 'Não há tarefas nesta lista.'})

    result = tarefas_schema.dump(all_tasks)
    return jsonify(result)

@app.route("/todolist/<id>/task/<id_task>", methods=['DELETE'])
@login_required
def delete_task(id, id_task):
    todolist = ListaDeTarefas.query.get(id)
    error = check_permission(todolist)
    if error:
        return error

    task = get_task_by_id(id_task)
    if task.lista_de_tarefas_id != int(id):
        return jsonify({'erro': 'Tarefa não encontrada nesta lista!'})

    db.session.delete(task)
    db.session.commit()
    return jsonify({'msg': 'Tarefa excluída com sucesso!'})

@app.route("/todolist/<id>/task/done", methods=['GET'])
@login_required
def get_task_done(id):
    return get_tasks_by_status(id, "Concluída")

@app.route("/todolist/<id>/task/doing", methods=['GET'])
@login_required
def get_task_doing(id):
    return get_tasks_by_status(id, "Fazendo")

@app.route("/todolist/<id>/task/todo", methods=['GET'])
@login_required
def get_task_todo(id):
    return get_tasks_by_status(id, "A fazer")

    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para ver tarefas desta lista!'})    

    all_tasks_todo = Tarefa.query.filter_by(status="A fazer", lista_de_tarefas_id=id).all()
    
    if not all_tasks_todo:
        return jsonify({'msg': 'Não há tarefas a fazer nesta lista.'})
    
    result = tarefas_schema.dump(all_tasks_todo)
    return jsonify(result)