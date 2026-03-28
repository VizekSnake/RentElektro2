"""add rental lifecycle fields

Revision ID: 20260328_0001
Revises:
Create Date: 2026-03-28 18:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260328_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("rentals", sa.Column("is_paid", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("rentals", sa.Column("paid_at", sa.DateTime(), nullable=True))
    op.add_column("rentals", sa.Column("handed_over_at", sa.DateTime(), nullable=True))
    op.add_column("rentals", sa.Column("returned_at", sa.DateTime(), nullable=True))

    op.execute(
        """
        UPDATE rentals
        SET is_paid = CASE
            WHEN status IN ('paid_not_rented', 'paid_rented', 'fulfilled') THEN TRUE
            ELSE FALSE
        END
        """
    )
    op.execute(
        """
        UPDATE rentals
        SET handed_over_at = COALESCE(handed_over_at, start_date)
        WHERE status IN ('paid_rented', 'fulfilled')
        """
    )
    op.execute(
        """
        UPDATE rentals
        SET returned_at = COALESCE(returned_at, end_date)
        WHERE status = 'fulfilled'
        """
    )


def downgrade() -> None:
    op.drop_column("rentals", "returned_at")
    op.drop_column("rentals", "handed_over_at")
    op.drop_column("rentals", "paid_at")
    op.drop_column("rentals", "is_paid")
