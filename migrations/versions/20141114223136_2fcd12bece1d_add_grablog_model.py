"""Add GrabLog model.

Revision ID: 2fcd12bece1d
Revises: 362dcae1d3d
Create Date: 2014-11-14 22:31:36.878038

"""

# revision identifiers, used by Alembic.
revision = '2fcd12bece1d'
down_revision = '362dcae1d3d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grab_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('error', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blog_id'], ['blog.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('grab_log')
    ### end Alembic commands ###
