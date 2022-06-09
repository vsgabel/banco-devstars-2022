"""empty message

Revision ID: 4140ba72f9c8
Revises: a71112cb1e86
Create Date: 2022-06-03 20:41:34.535003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4140ba72f9c8'
down_revision = 'a71112cb1e86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('perm', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('roles', 'perm')
    # ### end Alembic commands ###
