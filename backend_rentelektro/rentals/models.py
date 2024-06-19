from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, ForeignKey, DateTime
from core.database import Base
from enum import Enum as PyEnum



class AcceptedEnum(PyEnum):
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
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tool_id = Column(Integer, ForeignKey("tools.id"))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime,nullable=False)
    comment = Column(String, nullable=True)
    owner_comment = Column(String, nullable=True)
    status = Column(SQLAlchemyEnum(AcceptedEnum))