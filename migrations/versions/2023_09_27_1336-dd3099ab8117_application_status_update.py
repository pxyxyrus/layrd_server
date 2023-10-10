"""application_status_update

Revision ID: dd3099ab8117
Revises: 717e6ff2ebb7
Create Date: 2023-09-27 13:36:43.022344

"""
from alembic import op
import sqlalchemy as sa
from server.types import ApplicationStatus



# revision identifiers, used by Alembic.
revision = 'dd3099ab8117'
down_revision = '717e6ff2ebb7'
branch_labels = None
depends_on = None



def upgrade():
    table_name = "application"
    column_name = "status"

    enum_types_names = ApplicationStatus._member_names_
    enum_type_string = '"' + '", "'.join(enum_types_names) + '"'
    op.execute(f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} enum({enum_type_string});")
   
def downgrade():
    table_name = "application"
    column_name = "status"
    
    enum_types_names = ApplicationStatus._member_names_[:-1]
    enum_type_string = '"' + '", "'.join(enum_types_names) + '"'
    op.execute(f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} enum({enum_type_string});")