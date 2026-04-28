from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.reviews import service as reviews_service
from app.modules.reviews.schemas import Review, ReviewCreate

router = APIRouter()


@router.post("/reviews/", response_model=Review)
def add_review(review: ReviewCreate, db: Session = Depends(get_db)):
    return reviews_service.create_review(db=db, review=review)


@router.get("/reviews/{tool_id}/", response_model=dict)
def read_reviews(tool_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return reviews_service.get_reviews_summary(db, tool_id=tool_id, skip=skip, limit=limit)
