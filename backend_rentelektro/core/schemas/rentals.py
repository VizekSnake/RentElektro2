from typing import Any, Union, Annotated, List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field, PlainSerializer, AfterValidator, WithJsonSchema, ConfigDict
from enum import Enum, unique

def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]

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
    id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias="_id")
    tool_id: str
    user_id: str
    start_date: str
    end_date: str
    comment: Optional[str] = None
    owner_comment: Optional[str] = ""
    status: AcceptedEnum = AcceptedEnum.not_viewed

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: lambda x: str(x)}
    )


class RentalAdd(BaseModel):
    tool_id: str
    user_id: str
    start_date: str
    end_date: str
    comment: str

class RentalUpdate(BaseModel):
    tool_id: Optional[str] = None
    user_id: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    comment: Optional[str] = None

class RentalCollection(BaseModel):
    rentals: List[Rental]

