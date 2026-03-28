from __future__ import annotations

from enum import Enum as PyEnum
from datetime import datetime

from sqlalchemy import DateTime, Enum as SQLAlchemyEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

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


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tool_id: Mapped[int] = mapped_column(ForeignKey("tools.id"))
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
    is_paid: Mapped[bool] = mapped_column(default=False, server_default="0")
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    handed_over_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    returned_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    renter_seen_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
