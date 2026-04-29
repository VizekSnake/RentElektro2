import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.modules.reviews import repository
from app.modules.reviews.models import Review as ReviewModel
from app.modules.reviews.schemas import ReviewCreate, ReviewSummary
from app.modules.tools.models import Tool as ToolModel


def create_review(db: Session, review: ReviewCreate, user_id: uuid.UUID) -> ReviewModel:
    tool = db.get(ToolModel, review.tool_id)
    if tool is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    if tool.owner_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot review your own tool.",
        )
    if repository.get_for_tool_by_user(db, review.tool_id, user_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already reviewed this tool.",
        )

    db_review = ReviewModel(**review.model_dump(), user_id=user_id)
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


def get_reviews_summary(
    db: Session, tool_id: uuid.UUID, skip: int = 0, limit: int = 10
) -> ReviewSummary:
    tool = db.get(ToolModel, tool_id)
    if tool is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")

    reviews = repository.list_for_tool(db, tool_id=tool_id, skip=skip, limit=limit)
    total_reviews = repository.count_for_tool(db, tool_id)
    average_rating = repository.get_average_rating_for_tool(db, tool_id)

    comments = [review.comment for review in reviews if review.comment is not None]
    return ReviewSummary(
        comments=comments,
        average_rating=average_rating,
        total_reviews=total_reviews,
    )
