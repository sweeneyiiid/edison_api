"""empty message

Revision ID: beae7c5a838b
Revises: 52107d85c508
Create Date: 2020-04-13 12:32:25.713903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'beae7c5a838b'
down_revision = '52107d85c508'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('city', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('ext_key', sa.Integer(), nullable=False))
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
    op.drop_column('user', 'city')
    # ### end Alembic commands ###