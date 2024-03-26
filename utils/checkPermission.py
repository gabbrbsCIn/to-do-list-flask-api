from flask_login import login_user, login_required, logout_user, current_user
from flask import jsonify


def check_permission(todolist):
    if todolist is None:
        return jsonify({'erro': 'Lista de Tarefa não encontrada!'})
    if todolist.usuario_id != current_user.id:
        return jsonify({'erro': 'Você não tem permissão para alterar tarefas desta lista!'})
