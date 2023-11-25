"""update_project_status

Revision ID: 85977ff19cca
Revises: 6b7cd0e537cf
Create Date: 2023-11-24 01:22:35.699498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85977ff19cca'
down_revision = '6b7cd0e537cf'
branch_labels = None
depends_on = None



table_name = "project"
column_name = "status"

def upgrade() -> None:
    from server.types import ProjectStatus

    enum_types_names = ProjectStatus._member_names_
    enum_type_string = '"' + '", "'.join(enum_types_names) + '"'
    op.execute(f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} enum({enum_type_string});")

    op.alter_column(
        table_name,
        column_name,
        existing_type=sa.Enum(ProjectStatus),
        default=ProjectStatus.saved.value,
        server_default=sa.text("'saved'"),
        nullable=False,
        existing_nullable=False
    )


def downgrade() -> None:

    # to rollback
    import enum

    class ProjectStatus(enum.Enum):
        open = 'open' # project is taking applicants
        withdrawn = 'withdrawn' # project was withdrawn
        closed = 'closed' # project is no more taking applicants()
        ongoing = 'ongoing' # staking happened
        successful = 'successful' # project successfully finished
        unsuccessful = 'unsuccessful' # project aborted by someone
    
    enum_types_names = ProjectStatus._member_names_
    enum_type_string = '"' + '", "'.join(enum_types_names) + '"'
    op.execute(f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} enum({enum_type_string});")

    op.alter_column(
        table_name,
        column_name,
        existing_type=sa.Enum(ProjectStatus),
        default=ProjectStatus.open,
        server_default=sa.text("'open'"),
        nullable=False,
        existing_nullable=False
    )
