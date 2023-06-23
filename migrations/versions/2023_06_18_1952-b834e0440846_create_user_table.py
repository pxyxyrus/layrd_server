"""create user table

Revision ID: b834e0440846
Revises: 
Create Date: 2023-06-18 19:52:32.875204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b834e0440846'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('uid', sa.String(40), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(255), nullable=True),
        sa.Column('last_name', sa.String(255), nullable=True),
        sa.Column('city', sa.String(255), nullable=True),
        sa.Column('state', sa.String(2), nullable=True),
        sa.Column('zipcode', sa.String(5), nullable=True),
        sa.Column('user_type', sa.String(255), nullable=True)
    )


def downgrade() -> None:
    op.drop_table('user')
