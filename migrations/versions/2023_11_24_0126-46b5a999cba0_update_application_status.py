"""update_application_status

Revision ID: 46b5a999cba0
Revises: 46d9f4d44a9e
Create Date: 2023-11-25 01:24:16.855398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46b5a999cba0'
down_revision = '46d9f4d44a9e'
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
        server_default=sa.text("'saved'"),
        nullable=False,
        existing_nullable=False
    )
   
def downgrade():
    table_name = "application"
    column_name = "status"

    # to rollback
    import enum
    class ApplicationStatus(enum.Enum):
        applied = 'applied' # application is pending
        accepted = 'accepted' # application accepted by the project
        rejected = 'rejected' # applicant rejected the project offer
        confirmed = 'confirmed' # applicant confirmed joining the project
        withdrawn = 'withdrawn' # applicant withdrew from the project
    
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
