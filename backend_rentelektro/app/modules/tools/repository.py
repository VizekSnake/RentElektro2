from sqlalchemy.orm import Session

from app.modules.tools.models import Category as CategoryModel
from app.modules.tools.models import Tool as ToolModel


def get_tool_by_id(db: Session, tool_id: int) -> ToolModel | None:
    return db.query(ToolModel).filter(ToolModel.id == tool_id).first()


def get_tool_by_id_for_owner(db: Session, tool_id: int, owner_id: int) -> ToolModel | None:
    return (
        db.query(ToolModel)
        .filter(ToolModel.id == tool_id, ToolModel.owner_id == owner_id)
        .first()
    )


def list_tools(db: Session) -> list[ToolModel]:
    return db.query(ToolModel).all()


def list_categories(db: Session) -> list[CategoryModel]:
    return db.query(CategoryModel).all()
