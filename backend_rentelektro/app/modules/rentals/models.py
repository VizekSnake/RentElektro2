from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum as PyEnum

from nanoid import generate
from sqlalchemy import DateTime, Enum as SQLAlchemyEnum, ForeignKey, String, false
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from app.core.database import Base


class AcceptedEnum(str, PyEnum):
    accepted = "accepted"
    rejected_by_owner = "rejected_by_owner"
    canceled = "canceled"
    fulfilled = "fulfilled"
    paid_rented = "paid_rented"
    paid_not_rented = "paid_not_rented"
    viewed = "viewed"
    not_viewed = "not_viewed"
    problem = "problem"
    scam = "scam"


def generate_offer_number() -> str:
    return f"REN-{generate(alphabet='ABCDEFGHJKLMNPQRSTUVWXYZ23456789', size=6)}"


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4, index=True, unique=True
    )
    public_id: Mapped[str] = mapped_column(
        String(12),
        unique=True,
        index=True,
        nullable=False,
        default=generate_offer_number,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"))
    tool_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("tools.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        index=True,
    )
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
    owner_comment: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[AcceptedEnum] = mapped_column(
        SQLAlchemyEnum(AcceptedEnum),
        nullable=False,
        default=AcceptedEnum.not_viewed,
        server_default=AcceptedEnum.not_viewed.value,
    )
    is_paid: Mapped[bool] = mapped_column(default=False, server_default=false())
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    handed_over_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    returned_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    renter_seen_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
