"""update_application

Revision ID: 767ce7fe7137
Revises: 3332bee095c5
Create Date: 2023-08-12 16:18:59.122118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '767ce7fe7137'
down_revision = '3332bee095c5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    table_name = "application"
    column_name = "post_date"
    op.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} SET DEFAULT (UNIX_TIMESTAMP());")

def downgrade() -> None:
    table_name = "application"
    column_name = "post_date"
    op.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} DROP DEFAULT;")
