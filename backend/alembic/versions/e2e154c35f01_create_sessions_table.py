"""Create sessions table

Revision ID: e2e154c35f01
Revises: 098bb2dcaa27
Create Date: 2024-07-26 10:43:00

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = 'e2e154c35f01'
down_revision = '098bb2dcaa27'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Drop the table if it already exists
    conn = op.get_bind()
    if 'sessions' in conn.dialect.get_table_names(conn):
        op.drop_table('sessions')

    # Create sessions table
    op.create_table(
        'sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=False),
    )

def downgrade() -> None:
    # Drop the sessions table during downgrade
    conn = op.get_bind()
    if 'sessions' in conn.dialect.get_table_names(conn):
        op.drop_table('sessions')
