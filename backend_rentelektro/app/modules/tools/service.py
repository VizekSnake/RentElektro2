import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.modules.tools import repository
from app.modules.tools.models import Category as CategoryModel
from app.modules.tools.models import Tool as ToolModel
from app.modules.tools.schemas import CategoryAdd, ToolAdd, ToolUpdate

logger = logging.getLogger(__name__)


def create_tool(db: Session, tool: ToolAdd, user_id: int) -> ToolModel:
    logger.info("create_tool_attempt owner_id=%s type=%s brand=%s", user_id, tool.Type, tool.Brand)
    db_tool = ToolModel(**tool.model_dump(exclude={"owner_id"}), owner_id=user_id)
    db.add(db_tool)
    try:
        db.commit()
        db.refresh(db_tool)
        logger.info("create_tool_success tool_id=%s owner_id=%s", db_tool.id, user_id)
        return db_tool
    except IntegrityError as exc:
        db.rollback()
        logger.warning("create_tool_integrity_error owner_id=%s type=%s", user_id, tool.Type)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error adding tool",
        ) from exc


def create_category(db: Session, category: CategoryAdd, user_id: int) -> CategoryModel:
    logger.info("create_category_attempt creator_id=%s name=%s", user_id, category.name)
    db_category = CategoryModel(**category.model_dump(), creator_id=user_id)
    db.add(db_category)
    try:
        db.commit()
        db.refresh(db_category)
        logger.info("create_category_success category_id=%s creator_id=%s", db_category.id, user_id)
        return db_category
    except IntegrityError as exc:
        db.rollback()
        logger.warning("create_category_integrity_error creator_id=%s name=%s", user_id, category.name)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error adding category",
        ) from exc


def get_tool_or_404(db: Session, tool_id: int) -> ToolModel:
    db_tool = repository.get_tool_by_id(db, tool_id)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return db_tool


def get_owned_tool_or_404(db: Session, tool_id: int, owner_id: int) -> ToolModel:
    db_tool = repository.get_tool_by_id_for_owner(db, tool_id, owner_id)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return db_tool


def list_tools_or_404(db: Session) -> list[ToolModel]:
    tools = repository.list_tools(db)
    if not tools:
        raise HTTPException(status_code=404, detail="Tools not found")
    return tools


def list_categories_or_404(db: Session) -> list[CategoryModel]:
    categories = repository.list_categories(db)
    if not categories:
        raise HTTPException(status_code=404, detail="Categories not found")
    return categories


def update_tool(db: Session, tool_id: int, tool_update: ToolUpdate, owner_id: int) -> ToolModel:
    logger.info("update_tool_attempt tool_id=%s owner_id=%s", tool_id, owner_id)
    db_tool = get_owned_tool_or_404(db, tool_id, owner_id)
    update_data = tool_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tool, field, value)
    try:
        db.commit()
        db.refresh(db_tool)
        logger.info("update_tool_success tool_id=%s owner_id=%s", tool_id, owner_id)
        return db_tool
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("update_tool_db_error tool_id=%s owner_id=%s", tool_id, owner_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc


def delete_tool(db: Session, tool_id: int, owner_id: int) -> None:
    logger.info("delete_tool_attempt tool_id=%s owner_id=%s", tool_id, owner_id)
    db_tool = get_owned_tool_or_404(db, tool_id, owner_id)
    try:
        db.delete(db_tool)
        db.commit()
        logger.info("delete_tool_success tool_id=%s owner_id=%s", tool_id, owner_id)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("delete_tool_db_error tool_id=%s owner_id=%s", tool_id, owner_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc
