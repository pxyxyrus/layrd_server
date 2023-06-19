"""create project table

Revision ID: ee10cb6de4b6
Revises: b834e0440846
Create Date: 2023-06-18 21:01:50.708093

"""
from alembic import op
import sqlalchemy as sa
import enum

# revision identifiers, used by Alembic.
revision = 'ee10cb6de4b6'
down_revision = 'b834e0440846'
branch_labels = None
depends_on = None


class WorkLocation(enum.Enum):
    on_site = 1
    remote = 2
    hybrid = 3



def upgrade() -> None:
    op.create_table(
        'PROJECT',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('city', sa.String(255), nullable=False),
        sa.Column('state', sa.String(2), nullable=False),
        sa.Column('zipcode', sa.String(5), nullable=False),
        sa.Column('recruitment_type', sa.String(255), nullable=False),
        sa.Column('app_type', sa.String(255), nullable=False),
        sa.Column('participant_num', sa.Integer(), nullable=False),
        sa.Column('work_location', sa.Enum(WorkLocation), nullable=False),
        sa.Column('topics', sa.UnicodeText(), nullable=False),
        sa.Column('start_date', sa.DATETIME(), nullable=False),
        sa.Column('end_date', sa.DATETIME(), nullable=False),
        sa.Column('work_time_per_day', sa.Integer(), nullable=False),
        sa.Column('description', sa.UnicodeText(), nullable=False),
        sa.Column('required_qualifications', sa.UnicodeText(), nullable=True),
        sa.Column('optional_qualifications', sa.UnicodeText(), nullable=True),
        sa.Column('questions', sa.UnicodeText(), nullable=True),
        sa.Column('notes', sa.UnicodeText(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('PROJECT')
