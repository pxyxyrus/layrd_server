"""update_application

Revision ID: 46d9f4d44a9e
Revises: ba4e6efd52d7
Create Date: 2023-11-24 01:24:00.288725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46d9f4d44a9e'
down_revision = 'ba4e6efd52d7'
branch_labels = None
depends_on = None


table_name = "application"

def upgrade() -> None:
    op.alter_column(table_name, "resume_link", nullable=True, existing_type=sa.UnicodeText(), existing_nullable=False)
    op.alter_column(table_name, "reference_link", nullable=True, existing_type=sa.UnicodeText(), existing_nullable=False)
    


def downgrade() -> None:
    op.alter_column(table_name, "reference_link", nullable=False, existing_type=sa.UnicodeText(), existing_nullable=True)
    op.alter_column(table_name, "resume_link", nullable=False, existing_type=sa.UnicodeText(), existing_nullable=True)
    