from sqlalchemy.orm import Session
from reviews.models import Review
from reviews.schemas import ReviewCreate

def create_review(db: Session, review: ReviewCreate):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews(db: Session, tool_id: int, skip: int = 0, limit: int = 10):
    return db.query(Review).filter(Review.tool_id == tool_id).offset(skip).limit(limit).all()