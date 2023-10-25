"""create_main_tables
 
Revision ID: ea7f8663405c
Revises: 
Create Date: 2023-10-25 22:58:40.668798
 
"""
from alembic import op
import sqlalchemy as sa

 
# revision identifiers, used by Alembic
revision = 'ea7f8663405c'
down_revision = None
branch_labels = None
depends_on = None
 
 
def create_cleanings_table() -> None:
    op.create_table(
        "cleanings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("cleaning_type", sa.Text, nullable=False, server_default="spot_clean"),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
    )
 
 
def upgrade() -> None:
    create_cleanings_table()
 
 
def downgrade() -> None:
    op.drop_table("cleanings")