"""added username

Revision ID: 1543bfbc7a4d
Revises: e48aeda5899c
Create Date: 2022-08-31 16:16:52.958542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1543bfbc7a4d'
down_revision = 'e48aeda5899c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=20), nullable=False))
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###
