"""application_status_update

Revision ID: dd3099ab8117
Revises: 717e6ff2ebb7
Create Date: 2023-09-27 13:36:43.022344

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = 'dd3099ab8117'
down_revision = '717e6ff2ebb7'
branch_labels = None
depends_on = None




def upgrade():
    table_name = "application"
    column_name = "status"


    from server.types import ApplicationStatus

    enum_types_names = ApplicationStatus._member_names_
    enum_type_string = '"' + '", "'.join(enum_types_names) + '"'
    op.execute(f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} enum({enum_type_string});")

    op.alter_column(
        table_name,
        column_name,
        existing_type=sa.Enum(ApplicationStatus),
        default=ApplicationStatus.applied.value,
        server_default=sa.text("'applied'"),
        nullable=False,
        existing_nullable=False
    )
   
def downgrade():
    table_name = "application"
    column_name = "status"

    # to rollback
    import enum
    class ApplicationStatus(enum.Enum):
        applied = 'applied'
        accepted = 'accepted'
        rejected = 'rejected'
        closed = 'closed'
    
    enum_types_names = ApplicationStatus._member_names_
    enum_type_string = '"' + '", "'.join(enum_types_names) + '"'
    op.execute(f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} enum({enum_type_string});")

    op.alter_column(
        table_name,
        column_name,
        existing_type=sa.Enum(ApplicationStatus),
        default=ApplicationStatus.applied.value,
        server_default=sa.text("'applied'"),
        nullable=False,
        existing_nullable=False
    )