"""Add ERC20 address to UserDb

Revision ID: 3907628e6d70
Revises: 8376147d53d2
Create Date: 2024-07-27 <time>

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3907628e6d70'
down_revision = '8376147d53d2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('erc20_address', sa.String(), nullable=True))


def downgrade():
    op.drop_column('users', 'erc20_address')
