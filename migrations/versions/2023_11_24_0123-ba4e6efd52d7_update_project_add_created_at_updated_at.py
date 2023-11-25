"""update_project_add_created_at_updated_at

Revision ID: ba4e6efd52d7
Revises: 85977ff19cca
Create Date: 2023-11-24 23:38:56.783531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba4e6efd52d7'
down_revision = '85977ff19cca'
branch_labels = None
depends_on = None


table_name='project'

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


