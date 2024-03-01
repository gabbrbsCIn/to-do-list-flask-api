from flask import request, jsonify, render_template
from app import app, db, bcrypt
from models import Usuario, ListaDeTarefas, Tarefa
from flask_login import login_user, login_required, logout_user, current_user
from schemas import *



#Rotas da Tarefa
@app.route("/todolist/<id>/task", methods=['POST'])
@login_required
def add_task(id):
    todolist = ListaDeTarefas.query.get(id)

    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para adicionar tarefas a esta lista!'})    

    titulo = request.json["titulo"]  
    descricao = request.json.get("descricao")
    status = "A fazer"
    prazo_final = request.json.get("prazo_final")
    prioridade = request.json.get("prioridade")
    if prioridade == None:
        prioridade = 4

    new_task = Tarefa(titulo, descricao, status, prazo_final, prioridade, id)
    db.session.add(new_task)
    db.session.commit()

    return tarefa_schema.jsonify(new_task)

@app.route("/todolist/<id>/task/<id_task>/doing", methods=['PUT'])
@login_required
def update_status_task_doing(id, id_task):

    todolist = ListaDeTarefas.query.get(id)

    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para alterar tarefas desta lista!'})    

    task = Tarefa.query.get(id_task)

    if task is None:
        return jsonify({'erro': 'Tarefa não encontrada!'})
    
    if task.lista_de_tarefas_id != int(id):
        return jsonify({'erro': 'Tarefa não encontrada nesta lista!'})

    task.status = "Fazendo"
    db.session.commit()
    return tarefa_schema.jsonify(task)


@app.route("/todolist/<id>/task/<id_task>/done", methods=['PUT'])
@login_required
def update_status_task_done(id, id_task):

    todolist = ListaDeTarefas.query.get(id)

    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para alterar tarefas desta lista!'})    

    task = Tarefa.query.get(id_task)

    if task is None:
        return jsonify({'erro': 'Tarefa não encontrada!'})
    
    if task.lista_de_tarefas_id != int(id):
        return jsonify({'erro': 'Tarefa não encontrada nesta lista!'})

    task.status = "Concluída"

    db.session.commit()	
    return tarefa_schema.jsonify(task)

@app.route("/todolist/<id>/task/<id_task>", methods=['PUT'])
@login_required
def update_task_priority(id, id_task):

    todolist = ListaDeTarefas.query.get(id)

    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para alterar tarefas desta lista!'})    

    task = Tarefa.query.get(id_task)

    if task is None:
        return jsonify({'erro': 'Tarefa não encontrada!'})
    
    
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
def get_task(id):
    todolist = ListaDeTarefas.query.get(id)

    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para ver tarefas desta lista!'})    

    all_tasks = Tarefa.query.filter_by(lista_de_tarefas_id=id).all()
    result = tarefas_schema.dump(all_tasks)
    return jsonify(result)

@app.route("/todolist/<id>/task/<id_task>", methods=['DELETE'])
@login_required
def delete_task(id, id_task):

    todolist = ListaDeTarefas.query.get(id)

    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para excluir tarefas desta lista!'})    

    task = Tarefa.query.get(id_task)

    if task is None:
        return jsonify({'erro': 'Tarefa não encontrada!'})
    
    if task.lista_de_tarefas_id != int(id):
        return jsonify({'erro': 'Tarefa não encontrada nesta lista!'})

    db.session.delete(task)
    db.session.commit()
    return jsonify({'msg': 'Tarefa excluída com sucesso!'})

@app.route("/todolist/<id>/task/done", methods=['GET'])
@login_required
def get_task_done(id):
    todolist = ListaDeTarefas.query.get(id)

    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para ver tarefas desta lista!'})    

    all_tasks_done = Tarefa.query.filter_by(status="Concluída", lista_de_tarefas_id=id).all()

    if not all_tasks_done:
        return jsonify({'msg': 'Não há tarefas concluídas nesta lista de tarefas.'})

    result = tarefas_schema.dump(all_tasks_done)
    return jsonify(result)

@app.route("/todolist/<id>/task/doing", methods=['GET'])
@login_required
def get_task_doing(id):
    todolist = ListaDeTarefas.query.get(id)

    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para ver tarefas desta lista!'})    

    all_tasks_doing = Tarefa.query.filter_by(status="Fazendo", lista_de_tarefas_id=id).all()
    
    if not all_tasks_doing:
        return jsonify({'msg': 'Não há tarefas em andamento nesta lista de tarefas.'})
    
    result = tarefas_schema.dump(all_tasks_doing)
    return jsonify(result)

@app.route("/todolist/<id>/task/todo", methods=['GET'])
@login_required
def get_task_todo(id):
    todolist = ListaDeTarefas.query.get(id)

    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para ver tarefas desta lista!'})    

    all_tasks_todo = Tarefa.query.filter_by(status="A fazer", lista_de_tarefas_id=id).all()
    
    if not all_tasks_todo:
        return jsonify({'msg': 'Não há tarefas a fazer nesta lista.'})
    
    result = tarefas_schema.dump(all_tasks_todo)
    return jsonify(result)