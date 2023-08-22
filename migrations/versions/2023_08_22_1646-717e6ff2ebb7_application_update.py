"""application_update

Revision ID: 717e6ff2ebb7
Revises: 767ce7fe7137
Create Date: 2023-08-22 16:46:31.479683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '717e6ff2ebb7'
down_revision = '767ce7fe7137'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('application', sa.Column('reference_link', sa.UnicodeTdeext(), nullable=False, server_default=sa.text("('layrd.xyz')")))
    op.alter_column('application', 'reference_link', nullable=False, server_default=None, existing_server_default=sa.text("('layrd.xyz')"), existing_type=sa.UnicodeText())
    

def downgrade() -> None:
    op.drop_column('application', 'reference_link')
