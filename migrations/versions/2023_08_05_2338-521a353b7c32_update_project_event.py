"""update_project_event

Revision ID: 521a353b7c32
Revises: f74e6c0cf671
Create Date: 2023-08-05 23:38:16.796621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '521a353b7c32'
down_revision = 'f74e6c0cf671'
branch_labels = None
depends_on = None


def upgrade() -> None:
    default_val = False
    op.add_column('project', sa.Column("with_event", sa.Boolean(), server_default=sa.text(f"{default_val}"), default=default_val, nullable=False))
    op.execute(f"UPDATE project SET with_event={default_val}")
    op.add_column('project', sa.Column("event_name", sa.UnicodeText(), nullable=True))
    op.add_column('project', sa.Column("event_link", sa.UnicodeText(), nullable=True))
    


def downgrade() -> None:
    op.drop_column('project', "event_link")
    op.drop_column('project', "event_name")
    op.drop_column('project', "with_event")