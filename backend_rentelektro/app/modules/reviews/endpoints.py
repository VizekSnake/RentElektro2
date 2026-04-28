from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.modules.reviews import service as reviews_service
from app.modules.reviews.schemas import Review, ReviewCreate, ReviewSummary
from app.modules.users.models import User as UserModel

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("", response_model=Review, status_code=status.HTTP_201_CREATED)
def add_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    return reviews_service.create_review(db=db, review=review, user_id=user.id)


@router.get("/{tool_id}", response_model=ReviewSummary)
def read_reviews(
    tool_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return reviews_service.get_reviews_summary(db, tool_id=tool_id, skip=skip, limit=limit)
