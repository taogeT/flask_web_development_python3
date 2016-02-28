"""empty message

Revision ID: 1c7e7c88bbb0
Revises: c4f7a5abe0d9
Create Date: 2016-02-27 22:03:52.697644

"""

# revision identifiers, used by Alembic.
revision = '1c7e7c88bbb0'
down_revision = 'c4f7a5abe0d9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.Text(), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('location', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('member_since', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('name', sa.String(length=64), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'name')
    op.drop_column('user', 'member_since')
    op.drop_column('user', 'location')
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    ### end Alembic commands ###