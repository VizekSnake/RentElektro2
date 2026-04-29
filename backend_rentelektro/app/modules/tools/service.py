import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.model_utils import apply_update
from app.modules.tools import repository
from app.modules.tools.models import Category as CategoryModel, Tool as ToolModel
from app.modules.tools.schemas import (
    CategoryAdd,
    PaginatedTools,
    Tool,
    ToolAdd,
    ToolListFilters,
    ToolUpdate,
)

logger = logging.getLogger(__name__)


def create_tool(db: Session, tool: ToolAdd, user_id: UUID) -> ToolModel:
    logger.info("create_tool_attempt owner_id=%s type=%s brand=%s", user_id, tool.Type, tool.Brand)
    db_tool = ToolModel(
        **tool.model_dump(exclude={"owner_id", "TypeLabel", "PowerSourceLabel"}),
        owner_id=user_id,
    )
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


def create_category(db: Session, category: CategoryAdd, user_id: UUID) -> CategoryModel:
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
        logger.warning(
            "create_category_integrity_error creator_id=%s name=%s", user_id, category.name
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error adding category",
        ) from exc


def get_tool_or_404(db: Session, tool_id: UUID) -> ToolModel:
    db_tool = repository.get_tool_by_id(db, tool_id)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return db_tool


def get_owned_tool_or_404(db: Session, tool_id: UUID, owner_id: UUID) -> ToolModel:
    db_tool = repository.get_tool_by_id_for_owner(db, tool_id, owner_id)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return db_tool


def list_tools_or_404(db: Session, filters: ToolListFilters) -> PaginatedTools:
    tools, total = repository.list_tools(db, filters)
    if not tools and total == 0:
        raise HTTPException(status_code=404, detail="Tools not found")
    total_pages = max(1, (total + filters.page_size - 1) // filters.page_size)
    return PaginatedTools(
        items=[Tool.model_validate(tool, from_attributes=True) for tool in tools],
        total=total,
        page=filters.page,
        page_size=filters.page_size,
        total_pages=total_pages,
    )


def list_categories_or_404(db: Session) -> list[CategoryModel]:
    categories = repository.list_categories(db)
    if not categories:
        raise HTTPException(status_code=404, detail="Categories not found")
    return categories


def list_owner_tools(db: Session, owner_id: UUID) -> list[ToolModel]:
    return repository.list_tools_for_owner(db, owner_id)


def update_tool(db: Session, tool_id: UUID, tool_update: ToolUpdate, owner_id: UUID) -> ToolModel:
    logger.info("update_tool_attempt tool_id=%s owner_id=%s", tool_id, owner_id)
    db_tool = get_owned_tool_or_404(db, tool_id, owner_id)
    apply_update(db_tool, tool_update)
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


def delete_tool(db: Session, tool_id: UUID, owner_id: UUID) -> None:
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
