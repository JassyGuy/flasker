"""empty message

Revision ID: 962d05f52563
Revises: 252ad603b2d8
Create Date: 2022-09-14 16:13:16.192639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '962d05f52563'
down_revision = '252ad603b2d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_pic', sa.String(length=300), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_pic')
    # ### end Alembic commands ###
