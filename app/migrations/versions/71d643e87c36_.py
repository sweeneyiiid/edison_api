"""empty message

Revision ID: 71d643e87c36
Revises: beae7c5a838b
Create Date: 2020-04-13 12:45:28.459433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71d643e87c36'
down_revision = 'beae7c5a838b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('ext_key', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('gender', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('party_type', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('province', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('village', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'village')
    op.drop_column('user', 'province')
    op.drop_column('user', 'party_type')
    op.drop_column('user', 'gender')
    op.drop_column('user', 'ext_key')
    # ### end Alembic commands ###
