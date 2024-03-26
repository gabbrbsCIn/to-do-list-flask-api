from flask import jsonify, request, jsonify
from models.tasks import Tarefa
from models.todolist import ListaDeTarefas
from schemas.tasks import tarefas_schema
from flask_login import current_user


def get_tasks_by_status(id, status):
    todolist = ListaDeTarefas.query.get(id)
    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para ver tarefas desta lista!'})
    all_tasks = Tarefa.query.filter_by(status=status, lista_de_tarefas_id=id).all()
    if not all_tasks:
        return jsonify({'msg': f'Não há tarefas {status} nesta lista de tarefas.'})
    result = tarefas_schema.dump(all_tasks)
    return jsonify(result)