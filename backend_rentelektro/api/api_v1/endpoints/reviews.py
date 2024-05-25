from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.schemas.reviews import Review, ReviewCreate
from crud.crud_reviews import get_reviews, create_review
from core.dependencies import get_db
from statistics import mean

from starlette.responses import JSONResponse

router = APIRouter()


@router.post("/reviews/", response_model=Review)
def add_review(review: ReviewCreate, db: Session = Depends(get_db)):
    return create_review(db=db, review=review)


@router.get("/reviews/{tool_id}/", response_model=dict)
def read_reviews(tool_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reviews = get_reviews(db, tool_id=tool_id, skip=skip, limit=limit)

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")

    comments = [review.comment for review in reviews if review.comment is not None]
    ratings = [review.rating for review in reviews if review.rating is not None]
    if ratings:
        average_rating = mean(ratings)
    else:
        average_rating = None
    response = JSONResponse(content={"comments": comments, "average_rating": average_rating})
    return response
