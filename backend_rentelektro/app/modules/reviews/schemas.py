import uuid
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    rating: Annotated[float, Field(ge=1.0, le=5.0)]
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    tool_id: uuid.UUID


class Review(ReviewBase):
    id: uuid.UUID
    tool_id: uuid.UUID
    user_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class ReviewSummary(BaseModel):
    comments: list[str]
    average_rating: float | None
    total_reviews: int
