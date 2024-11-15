"""Add Reactions Table.

Revision ID: bc75bc87b8fa
Revises: 84fe2c915d76
Create Date: 2024-11-09 12:09:09.732350

"""

import os

import sqlalchemy as sa
from alembic import op

environment = os.getenv('FLASK_ENV')
SCHEMA = os.environ.get('SCHEMA')

# revision identifiers, used by Alembic.
revision = 'bc75bc87b8fa'
down_revision = '84fe2c915d76'
branch_labels = None
depends_on = None


def upgrade():
	"""Create the reactions table for storing message reactions."""
	# ### commands auto generated by Alembic - please adjust! ###
	op.create_table(
		'reactions',
		sa.Column('id', sa.Integer(), nullable=False),
		sa.Column('user_id', sa.Integer(), nullable=False),
		sa.Column('message_id', sa.Integer(), nullable=False),
		sa.Column('emoji', sa.String(), nullable=False),
		sa.Column('created_at', sa.DateTime(), nullable=False),
		sa.Column('updated_at', sa.DateTime(), nullable=False),
		sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ondelete='CASCADE'),
		sa.ForeignKeyConstraint(
			['user_id'],
			['users.id'],
		),
		sa.PrimaryKeyConstraint('id'),
	)
	if environment == 'production':
		op.execute(f'ALTER TABLE reactions SET SCHEMA {SCHEMA};')
	# ### end Alembic commands ###


def downgrade():
	"""Remove the reactions table."""
	# ### commands auto generated by Alembic - please adjust! ###
	op.drop_table('reactions')


# ### end Alembic commands ###
