from sqlalchemy.orm import Session

from app.modules.reviews.models import Review as ReviewModel


def list_for_tool(db: Session, tool_id: int, skip: int = 0, limit: int = 10) -> list[ReviewModel]:
    return (
        db.query(ReviewModel).filter(ReviewModel.tool_id == tool_id).offset(skip).limit(limit).all()
    )
