"""add renter seen timestamp

Revision ID: 20260328_0002
Revises: 20260328_0001
Create Date: 2026-03-28 20:10:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260328_0002"
down_revision = "20260328_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("rentals", sa.Column("renter_seen_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("rentals", "renter_seen_at")
