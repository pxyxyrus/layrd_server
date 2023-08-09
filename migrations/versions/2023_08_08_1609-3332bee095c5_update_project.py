"""update project

Revision ID: 3332bee095c5
Revises: 521a353b7c32
Create Date: 2023-08-08 16:09:59.387961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3332bee095c5'
down_revision = '521a353b7c32'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('project', 'post_date', new_column_name='app_result_post_date', existing_type=sa.Integer(), nullable=False)
    table_name = 'project'
    column_name = 'post_date'
    # the following sql statement only works on mysql
    op.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} INTEGER NOT NULL DEFAULT (UNIX_TIMESTAMP());")
    


def downgrade() -> None:
    op.drop_column('project', 'post_date', nullable=False)
    op.alter_column('project', 'app_result_post_date', new_column_name='post_date', existing_type=sa.Integer(), nullable=False)
