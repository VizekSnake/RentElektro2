from datetime import date, datetime
from enum import Enum, unique
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator


@unique
class AcceptedEnum(str, Enum):
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


class Rental(BaseModel):
    rental_id: int
    tool_id: int
    user_id: int
    start_date: date
    end_date: date
    comment: Optional[str] = None
    owner_comment: Optional[str] = ""
    status: AcceptedEnum = AcceptedEnum.not_viewed

    model_config = ConfigDict(arbitrary_types_allowed=True)


class RentalAdd(BaseModel):
    tool_id: int
    user_id: int
    start_date: date
    end_date: date
    comment: str

    @field_validator("start_date", "end_date", mode="before")
    def parse_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value


class RentalUpdate(BaseModel):
    tool_id: Optional[int] = None
    user_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    comment: Optional[str] = None


class RentalCollection(BaseModel):
    rentals: List[Rental]
