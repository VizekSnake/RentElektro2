from pydantic import BaseModel, confloat, field_validator, ConfigDict
from typing import Optional


class ReviewBase(BaseModel):
    tool_id: int
    user_id: int
    rating: confloat(ge=1.0, le=5.0)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
