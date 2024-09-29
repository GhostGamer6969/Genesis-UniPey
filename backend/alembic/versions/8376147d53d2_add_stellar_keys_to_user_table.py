"""Add Stellar keys to user table

Revision ID: <8376147d53d2>
Revises: <e2e154c35f01>
Create Date: <timestamp>
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '8376147d53d2'
down_revision = 'e2e154c35f01'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('stellar_public_key', sa.String(), nullable=True))
    op.add_column('users', sa.Column('stellar_secret_key', sa.String(), nullable=True))
    op.add_column('users', sa.Column('erc20_address', sa.String(), nullable=True))

def downgrade():
    op.drop_column('users', 'stellar_public_key')
    op.drop_column('users', 'stellar_secret_key')
    op.drop_column('users', 'erc20_address')
