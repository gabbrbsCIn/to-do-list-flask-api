from models.tasks import Tarefa
from flask import jsonify


def get_task_by_id(id_task):
    task = Tarefa.query.get(id_task)
    if task is None:
        return jsonify({'erro': 'Tarefa não encontrada!'})
    return task