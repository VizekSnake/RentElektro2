from statistics import mean

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.modules.reviews import repository
from app.modules.reviews.models import Review as ReviewModel
from app.modules.reviews.schemas import ReviewCreate


def create_review(db: Session, review: ReviewCreate) -> ReviewModel:
    db_review = ReviewModel(**review.model_dump())
    db.add(db_review)
    try:
        db.commit()
        db.refresh(db_review)
        return db_review
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc


def get_reviews_summary(db: Session, tool_id: int, skip: int = 0, limit: int = 10) -> dict:
    reviews = repository.list_for_tool(db, tool_id=tool_id, skip=skip, limit=limit)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")

    comments = [review.comment for review in reviews if review.comment is not None]
    ratings = [review.rating for review in reviews if review.rating is not None]
    average_rating = mean(ratings) if ratings else None
    return {"comments": comments, "average_rating": average_rating}
