"""update project

Revision ID: f30ccd87d20c
Revises: 1081b0c2cecd
Create Date: 2023-07-05 00:22:00.520707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f30ccd87d20c'
down_revision = '1081b0c2cecd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('project', sa.Column("name", sa.String(255), nullable=False))
    op.add_column('project', sa.Column("organization", sa.String(255), nullable=False))
    op.add_column('project', sa.Column("skills", sa.UnicodeText(), nullable=False))
    op.add_column('project', sa.Column("app_close_date", sa.Integer(), nullable=False))
    op.add_column('project', sa.Column("post_date", sa.Integer(), nullable=False))
    op.drop_column('project', 'zipcode')
    op.drop_column('project', 'optional_qualifications')
    
    


def downgrade() -> None:
    op.add_column('project', sa.Column("optional_qualifications", sa.UnicodeText(), nullable=True))
    op.add_column("project", sa.Column("zipcode", sa.String(5), default="00000", server_default=sa.text("'00000'"), nullable=False))
    op.drop_column('project', 'post_date')
    op.drop_column('project', 'app_close_date')
    op.drop_column('project', 'skills')
    op.drop_column('project', 'organization')
    op.drop_column('project', 'name')
