from app import ma
from models import Usuario, ListaDeTarefas, Tarefa


class UsuarioSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'nome', 'email', 'senha')


class ListaDeTarefasSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'titulo', 'descricao', 'usuario_id')

class TarefaSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'titulo', 'descricao', 'status', 'prazo_final', 'prioridade')

tarefa_schema = TarefaSchema()
tarefas_schema = TarefaSchema(many=True)

listadetarefa_schema = ListaDeTarefasSchema()
listadetarefas_schema = ListaDeTarefasSchema(many=True)

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)