"""update_project

Revision ID: 55cede4d0888
Revises: dd3099ab8117
Create Date: 2023-11-22 11:15:06.201563

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '55cede4d0888'
down_revision = 'dd3099ab8117'
branch_labels = None
depends_on = None


table_name = "project"

def upgrade() -> None:

    # change columns to nullable
    from server.types import RecruitmentType
    from server.types import ApplicationType
    from server.types import WorkLocation
 
    op.alter_column(table_name, "city", nullable=True, existing_type=sa.String(255), existing_nullable=False)
    op.alter_column(table_name, "state", nullable=True, existing_type=sa.String(2), existing_nullable=False)
    op.alter_column(table_name, "recruitment_type", nullable=True, existing_type=sa.Enum(RecruitmentType), existing_nullable=False)
    op.alter_column(table_name, "app_type", nullable=True, existing_type=sa.Enum(ApplicationType), existing_nullable=False)
    op.alter_column(table_name, "participant_num", nullable=True, existing_type=sa.Integer(), existing_nullable=False)
    op.alter_column(table_name, "work_location", nullable=True, existing_type=sa.Enum(WorkLocation), existing_nullable=False)
    op.alter_column(table_name, "topics", nullable=True, existing_type=sa.UnicodeText(), existing_nullable=False)
    op.alter_column(table_name, "work_time_per_day", nullable=True, existing_type=sa.Integer(), existing_nullable=False)
    op.alter_column(table_name, "description", nullable=True, existing_type=sa.UnicodeText(), existing_nullable=False)
    op.alter_column(table_name, "notes", nullable=True, existing_type=sa.UnicodeText(), existing_nullable=False)
    op.alter_column(table_name, "name", nullable=True, existing_type=sa.String(255), existing_nullable=False)
    op.alter_column(table_name, "organization", nullable=True, existing_type=sa.String(255), existing_nullable=False)
    op.alter_column(table_name, "skills", nullable=True, existing_type=sa.UnicodeText(), existing_nullable=False)
    op.alter_column(table_name, "final_delivery_types", nullable=True, existing_type=sa.String(255), existing_nullable=False, existing_server_default=sa.text("'[\"other\", \"na\", \"na\"]'"))
    op.alter_column(table_name, "final_delivery_description", nullable=True, existing_type=sa.UnicodeText(), existing_nullable=False)








def downgrade() -> None:

    from server.types import RecruitmentType
    from server.types import ApplicationType
    from server.types import WorkLocation

    op.alter_column(table_name, "final_delivery_description", nullable=False, existing_type=sa.UnicodeText(), existing_nullable=True)
    op.alter_column(table_name, "final_delivery_types", nullable=False, existing_type=sa.String(255), existing_nullable=True, existing_server_default=sa.text("'[\"other\", \"na\", \"na\"]'"))
    op.alter_column(table_name, "skills", nullable=False, existing_type=sa.UnicodeText(), existing_nullable=True)
    op.alter_column(table_name, "organization", nullable=False, existing_type=sa.String(255), existing_nullable=True)
    op.alter_column(table_name, "name", nullable=False, existing_type=sa.String(255), existing_nullable=True)
    op.alter_column(table_name, "notes", nullable=False, existing_type=sa.UnicodeText(), existing_nullable=True)
    op.alter_column(table_name, "description", nullable=False, existing_type=sa.UnicodeText(), existing_nullable=True)
    op.alter_column(table_name, "work_time_per_day", nullable=False, existing_type=sa.Integer(), existing_nullable=True)
    op.alter_column(table_name, "topics", nullable=False, existing_type=sa.UnicodeText(), existing_nullable=True)
    op.alter_column(table_name, "work_location", nullable=False, existing_type=sa.Enum(WorkLocation), existing_nullable=True)
    op.alter_column(table_name, "participant_num", nullable=False, existing_type=sa.Integer(), existing_nullable=True)
    op.alter_column(table_name, "app_type", nullable=False, existing_type=sa.Enum(ApplicationType), existing_nullable=True)
    op.alter_column(table_name, "recruitment_type", nullable=False, existing_type=sa.Enum(RecruitmentType), existing_nullable=True)
    op.alter_column(table_name, "state", nullable=False, existing_type=sa.String(2), existing_nullable=True)
    op.alter_column(table_name, "name", nullable=False, existing_type=sa.String(255), existing_nullable=True)



