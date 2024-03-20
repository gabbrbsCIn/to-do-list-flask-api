from app import ma


class TarefaSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'titulo', 'descricao', 'status', 'prazo_final', 'prioridade')

tarefa_schema = TarefaSchema()
tarefas_schema = TarefaSchema(many=True)