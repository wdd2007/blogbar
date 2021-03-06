"""Add pure_content to Post model.

Revision ID: 4c281030504f
Revises: 1888d7240e64
Create Date: 2014-11-26 15:18:05.386154

"""

# revision identifiers, used by Alembic.
revision = '4c281030504f'
down_revision = '1888d7240e64'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('pure_content', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'pure_content')
    ### end Alembic commands ###
