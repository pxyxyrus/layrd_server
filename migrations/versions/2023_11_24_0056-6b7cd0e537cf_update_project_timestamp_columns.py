"""update_project_timestamp_columns

Revision ID: 6b7cd0e537cf
Revises: 55cede4d0888
Create Date: 2023-11-24 00:56:03.862160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b7cd0e537cf'
down_revision = '55cede4d0888'
branch_labels = None
depends_on = None



table_name = "project"


def upgrade() -> None:
    # from int to timestamp update columns, and update to nullable
    timestamp_columns = ["start_date", "end_date", "app_close_date", "app_result_post_date"]
    for col in timestamp_columns:
        new_col_name = col + "2"
        op.add_column(table_name, sa.Column(new_col_name, sa.TIMESTAMP(), nullable=True))
        op.execute(f"UPDATE {table_name} SET {new_col_name} = FROM_UNIXTIME({col});")
        op.drop_column(table_name, col)
        op.alter_column(
            table_name,
            column_name=new_col_name,
            new_column_name=col,
            existing_nullable=True,
            existing_type=sa.TIMESTAMP()
        )



def downgrade() -> None:
    timestamp_columns = ["start_date", "end_date", "app_close_date", "app_result_post_date"]
    for col in timestamp_columns:
        new_col_name = col + "2"
        op.add_column(table_name, sa.Column(new_col_name, sa.Integer(), nullable=True))
        op.execute(f"UPDATE {table_name} SET {new_col_name} = UNIX_TIMESTAMP({col});")
        op.drop_column(table_name, col)
        op.alter_column(
            table_name,
            column_name=new_col_name,
            new_column_name=col,
            existing_nullable=True,
            existing_type=sa.Integer()
        )



