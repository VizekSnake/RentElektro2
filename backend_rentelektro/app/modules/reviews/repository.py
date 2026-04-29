import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.reviews.models import Review as ReviewModel


def get_for_tool_by_user(db: Session, tool_id: uuid.UUID, user_id: uuid.UUID) -> ReviewModel | None:
    return (
        db.query(ReviewModel)
        .filter(ReviewModel.tool_id == tool_id, ReviewModel.user_id == user_id)
        .first()
    )


def count_for_tool(db: Session, tool_id: uuid.UUID) -> int:
    return db.query(func.count(ReviewModel.id)).filter(ReviewModel.tool_id == tool_id).scalar() or 0


def get_average_rating_for_tool(db: Session, tool_id: uuid.UUID) -> float | None:
    return db.query(func.avg(ReviewModel.rating)).filter(ReviewModel.tool_id == tool_id).scalar()


def list_for_tool(
    db: Session, tool_id: uuid.UUID, skip: int = 0, limit: int = 10
) -> list[ReviewModel]:
    return (
        db.query(ReviewModel)
        .filter(ReviewModel.tool_id == tool_id)
        .order_by(ReviewModel.created_at.desc(), ReviewModel.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
