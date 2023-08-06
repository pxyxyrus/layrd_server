"""update_project

Revision ID: f74e6c0cf671
Revises: f30ccd87d20c
Create Date: 2023-08-01 15:55:41.313546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f74e6c0cf671'
down_revision = 'f30ccd87d20c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    default_val = "[\"other\", \"na\", \"na\"]"
    op.add_column('project', sa.Column("final_delivery_types", sa.String(255), server_default=sa.text(f"'{default_val}'"), default=default_val, nullable=False))
    op.execute(f"UPDATE project SET final_delivery_types='{default_val}'")
    default_val=""
    op.add_column('project', sa.Column("final_delivery_description", sa.UnicodeText(), nullable=False))
    op.execute(f"UPDATE project SET final_delivery_description='{default_val}'")
    


def downgrade() -> None:
    op.drop_column('project', "final_delivery_description")
    op.drop_column('project', "final_delivery_types")
