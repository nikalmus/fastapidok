"""add_cleaner_id_column_to_cleanings
 
Revision ID: 0af48385d186
Revises: 1f9900491837
Create Date: 2023-10-29 02:55:08.667741
 
"""
from alembic import op
import sqlalchemy as sa

 
# revision identifiers, used by Alembic
revision = '0af48385d186'
down_revision = '1f9900491837'
branch_labels = None
depends_on = None
 
 
def add_cleaner_id_column() -> None:
    op.add_column(
        "cleanings",
        sa.Column("cleaner_id", sa.Integer, sa.ForeignKey("cleaner.id"), nullable=True),
    )

def upgrade() -> None:
    add_cleaner_id_column()

def downgrade() -> None:
    op.drop_column("cleanings", "cleaner_id")