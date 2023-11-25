"""update_application_add_created_at_updated_at

Revision ID: 7bc6295d6d77
Revises: 46b5a999cba0
Create Date: 2023-11-24 23:39:07.534079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bc6295d6d77'
down_revision = '46b5a999cba0'
branch_labels = None
depends_on = None


table_name='application'


def upgrade() -> None:
    op.add_column(table_name, sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))
    op.add_column(table_name, sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')))
    
    op.execute(f"UPDATE {table_name} SET created_at = FROM_UNIXTIME(post_date);")
    op.execute(f"UPDATE {table_name} SET updated_at = FROM_UNIXTIME(post_date);")
    
    op.drop_column(table_name, 'post_date')


def downgrade() -> None:
    op.add_column(table_name, sa.Column('post_date', sa.Integer(), nullable=False, server_default=sa.text('(UNIX_TIMESTAMP())')))

    op.execute(f"UPDATE {table_name} SET post_date = UNIX_TIMESTAMP(created_at);")

    op.drop_column(table_name, "updated_at")
    op.drop_column(table_name, "created_at")