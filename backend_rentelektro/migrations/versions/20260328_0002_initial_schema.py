"""initial schema

Revision ID: 20260328_0002
Revises:
Create Date: 2026-04-28 17:10:00
"""

import sqlalchemy as sa
from alembic import op

revision = "20260328_0002"
down_revision = None
branch_labels = None
depends_on = None

accepted_enum = sa.Enum(
    "accepted",
    "rejected_by_owner",
    "canceled",
    "fulfilled",
    "paid_rented",
    "paid_not_rented",
    "viewed",
    "not_viewed",
    "problem",
    "scam",
    name="acceptedenum",
)


def upgrade() -> None:
    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tool_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("rating", sa.Float(), nullable=False),
        sa.Column("comment", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reviews_id", "reviews", ["id"], unique=False)
    op.create_index("ix_reviews_tool_id", "reviews", ["tool_id"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("firstname", sa.String(), nullable=False),
        sa.Column("lastname", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("company", sa.Boolean(), nullable=False),
        sa.Column("profile_picture", sa.String(), nullable=True),
        sa.Column("role", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("creator_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["creator_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_categories_id", "categories", ["id"], unique=True)

    op.create_table(
        "tools",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("Type", sa.String(), nullable=False),
        sa.Column("PowerSource", sa.String(), nullable=False),
        sa.Column("Brand", sa.String(), nullable=False),
        sa.Column("Description", sa.String(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("Availability", sa.Boolean(), nullable=False),
        sa.Column("Insurance", sa.Boolean(), nullable=False),
        sa.Column("Power", sa.Integer(), nullable=True),
        sa.Column("Age", sa.Float(), nullable=True),
        sa.Column("RatePerDay", sa.Float(), nullable=True),
        sa.Column("ImageURL", sa.String(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"]),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tools_id", "tools", ["id"], unique=False)

    op.create_table(
        "rentals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("tool_id", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.DateTime(), nullable=False),
        sa.Column("end_date", sa.DateTime(), nullable=False),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column("owner_comment", sa.String(), nullable=True),
        sa.Column(
            "status",
            accepted_enum,
            nullable=False,
            server_default=sa.text("'not_viewed'"),
        ),
        sa.Column("is_paid", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("paid_at", sa.DateTime(), nullable=True),
        sa.Column("handed_over_at", sa.DateTime(), nullable=True),
        sa.Column("returned_at", sa.DateTime(), nullable=True),
        sa.Column("renter_seen_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["tool_id"], ["tools.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rentals")
    op.drop_index("ix_tools_id", table_name="tools")
    op.drop_table("tools")
    op.drop_index("ix_categories_id", table_name="categories")
    op.drop_table("categories")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_index("ix_reviews_tool_id", table_name="reviews")
    op.drop_index("ix_reviews_id", table_name="reviews")
    op.drop_table("reviews")
