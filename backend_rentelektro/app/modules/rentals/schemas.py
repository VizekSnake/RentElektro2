from datetime import date, datetime
from typing import Literal, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)

from app.modules.rentals.models import AcceptedEnum


class Rental(BaseModel):
    id: int
    tool_id: int
    user_id: int
    start_date: date
    end_date: date
    comment: Optional[str] = None
    owner_comment: Optional[str] = ""
    status: AcceptedEnum = AcceptedEnum.not_viewed
    is_paid: bool = False
    paid_at: Optional[datetime] = None
    handed_over_at: Optional[datetime] = None
    returned_at: Optional[datetime] = None
    renter_seen_at: Optional[datetime] = None

    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)


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


class RentalDecisionUpdate(BaseModel):
    status: AcceptedEnum
    owner_comment: Optional[str] = None


class RentalPaymentUpdate(BaseModel):
    cardholder: str
    card_number: str
    expiry_date: str
    cvc: str


class RentalOwnerStatusUpdate(BaseModel):
    status: AcceptedEnum


class RentalInboxTool(BaseModel):
    id: int
    Type: str
    TypeLabel: Optional[str] = None
    Brand: str
    PowerSourceLabel: Optional[str] = None
    ImageURL: Optional[str] = None
    RatePerDay: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class RentalParticipant(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    email: str
    phone: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RentalInboxItem(BaseModel):
    id: int
    tool_id: int
    user_id: int
    start_date: date
    end_date: date
    comment: Optional[str] = None
    owner_comment: Optional[str] = None
    status: AcceptedEnum
    is_paid: bool = False
    paid_at: Optional[datetime] = None
    handed_over_at: Optional[datetime] = None
    returned_at: Optional[datetime] = None
    renter_seen_at: Optional[datetime] = None
    tool: RentalInboxTool
    requester: RentalParticipant
    owner: RentalParticipant

    model_config = ConfigDict(from_attributes=True)


class RentalNotificationsReadUpdate(BaseModel):
    scope: Literal["owner", "renter", "all"] = "all"


class RentalNotificationsReadResult(BaseModel):
    scope: Literal["owner", "renter", "all"]
    updated_owner: int
    updated_renter: int
