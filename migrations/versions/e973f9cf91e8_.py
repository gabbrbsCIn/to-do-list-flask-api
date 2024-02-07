"""empty message

Revision ID: e973f9cf91e8
Revises: 095924ecd8c4
Create Date: 2024-02-07 11:52:58.229065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e973f9cf91e8'
down_revision = '095924ecd8c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lista_de_tarefas', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_title_per_user', ['titulo', 'usuario_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lista_de_tarefas', schema=None) as batch_op:
        batch_op.drop_constraint('unique_title_per_user', type_='unique')

    # ### end Alembic commands ###