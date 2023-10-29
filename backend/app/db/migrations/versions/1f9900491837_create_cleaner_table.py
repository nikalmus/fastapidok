"""create_cleaner_table
 
Revision ID: 1f9900491837
Revises: ee95fc57690b
Create Date: 2023-10-29 02:49:55.032965
 
"""
from alembic import op
import sqlalchemy as sa

 
# revision identifiers, used by Alembic
revision = '1f9900491837'
down_revision = 'ee95fc57690b'
branch_labels = None
depends_on = None
 
 
def create_cleaner_table() -> None:
    op.create_table(
        "cleaner",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
    )

def upgrade() -> None:
    create_cleaner_table()

def downgrade() -> None:
    op.drop_table("cleaner")