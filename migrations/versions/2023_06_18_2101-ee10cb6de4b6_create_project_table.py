"""create project table

Revision ID: ee10cb6de4b6
Revises: b834e0440846
Create Date: 2023-06-18 21:01:50.708093

"""
from alembic import op
import sqlalchemy as sa


from server.types import RecruitmentType, ApplicationType, WorkLocation, ProjectStatus


# revision identifiers, used by Alembic.
revision = 'ee10cb6de4b6'
down_revision = 'b834e0440846'
branch_labels = None
depends_on = None





def upgrade() -> None:
    op.create_table(
        'project',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('city', sa.String(255), nullable=False),
        sa.Column('state', sa.String(2), nullable=False),
        sa.Column('zipcode', sa.String(5), nullable=False),
        sa.Column('recruitment_type', sa.Enum(RecruitmentType), nullable=False),
        sa.Column('app_type', sa.Enum(ApplicationType), nullable=False),
        sa.Column('participant_num', sa.Integer(), nullable=False),
        sa.Column('work_location', sa.Enum(WorkLocation), nullable=False),
        sa.Column('topics', sa.UnicodeText(), nullable=False),
        sa.Column('start_date', sa.Integer(), nullable=False),
        sa.Column('end_date', sa.Integer(), nullable=False),
        sa.Column('work_time_per_day', sa.Integer(), nullable=False),
        sa.Column('description', sa.UnicodeText(), nullable=False),
        sa.Column('required_qualifications', sa.UnicodeText(), nullable=True),
        sa.Column('optional_qualifications', sa.UnicodeText(), nullable=True),
        sa.Column('questions', sa.UnicodeText(), nullable=True),
        sa.Column('notes', sa.UnicodeText(), nullable=False),
        sa.Column('owner_uid', sa.String(40), nullable=False),
        sa.Column('status', sa.Enum(ProjectStatus), nullable=False, default=ProjectStatus.open, server_default=sa.text("'open'")),
        sa.Column('staked', sa.Boolean(), nullable=False, default=False, server_default=sa.text('FALSE'))
    )


def downgrade() -> None:
    op.drop_table('project')