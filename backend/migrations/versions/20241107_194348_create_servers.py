"""Create Servers Table.

Revision ID: f20fa35fc3d9
Revises: ffdc0a98111c
Create Date: 2024-11-07 19:43:48.395394

"""

import os

import sqlalchemy as sa
from alembic import op

environment = os.getenv('FLASK_ENV')
SCHEMA = os.environ.get('SCHEMA')

# revision identifiers, used by Alembic.
revision = 'f20fa35fc3d9'
down_revision = 'ffdc0a98111c'
branch_labels = None
depends_on = None


def upgrade():
	"""Create the servers table."""
	# ### commands auto generated by Alembic - please adjust! ###
	op.create_table(
		'servers',
		sa.Column('id', sa.Integer(), nullable=False),
		sa.Column('name', sa.String(length=100), nullable=False),
		sa.Column('description', sa.String(length=255), nullable=True),
		sa.Column('created_at', sa.DateTime(), nullable=False),
		sa.Column('updated_at', sa.DateTime(), nullable=False),
		sa.PrimaryKeyConstraint('id'),
	)

	if environment == 'production':
		op.execute(f'ALTER TABLE servers SET SCHEMA {SCHEMA};')
	# ### end Alembic commands ###


def downgrade():
	"""Remove the servers table."""
	# ### commands auto generated by Alembic - please adjust! ###
	op.drop_table('servers')
	# ### end Alembic commands ###
