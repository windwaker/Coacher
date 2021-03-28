"""Init database

Revision ID: a565b12469ed
Revises: 
Create Date: 2021-03-27 14:40:18.890359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a565b12469ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'players',
        sa.Column('id', sa.Integer, primary_key=True, unique=True),
        sa.Column('first_name', sa.String(100), unique=False),
        sa.Column('last_name', sa.String(100), unique=False),
        sa.Column('active', sa.Boolean, default=True),
        sa.Column('date_of_birth', sa.Date),
        sa.Column('created_date', sa.DateTime)
    )

    op.create_table(
        'guardians',
        sa.Column('id', sa.Integer, primary_key=True, unique=True),
        sa.Column('first_name', sa.String(100), unique=False),
        sa.Column('last_name', sa.String(100), unique=False),
        sa.Column('mobile_number', sa.String(20), unique=False),
        sa.Column('player_id', sa.Integer)
    )

    op.create_table(
        'addresses',

    )


def downgrade():
    pass
