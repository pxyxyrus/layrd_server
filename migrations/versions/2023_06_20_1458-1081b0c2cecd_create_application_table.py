"""create application table

Revision ID: 1081b0c2cecd
Revises: ee10cb6de4b6
Create Date: 2023-06-20 14:58:15.131115

"""
from alembic import op
import sqlalchemy as sa
from server.types import ApplicationStatus


# revision identifiers, used by Alembic.
revision = '1081b0c2cecd'
down_revision = 'ee10cb6de4b6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'application',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('owner_user_id', sa.Integer(), nullable=False),
        sa.Column('post_date', sa.Integer(), nullable=False),
        sa.Column('response', sa.UnicodeText(), nullable=True),
        sa.Column('comments', sa.UnicodeText(), nullable=True),
        sa.Column('resume_link', sa.UnicodeText(), nullable=False),
        sa.Column('status', sa.Enum(ApplicationStatus), default=ApplicationStatus.applied),
        sa.Column('staked', sa.Boolean(), default=False)
    )
    op.create_unique_constraint("one_proj_app_per_user", "application", ["project_id", "owner_user_id"])


def downgrade() -> None:
    op.drop_table('application')
