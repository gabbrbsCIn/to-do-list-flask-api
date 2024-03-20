from app import ma


class ListaDeTarefasSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'titulo', 'descricao', 'usuario_id')

listadetarefa_schema = ListaDeTarefasSchema()
listadetarefas_schema = ListaDeTarefasSchema(many=True)