from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.modules.tools.models import Category as CategoryModel
from app.modules.tools.models import Tool as ToolModel
from app.modules.tools.schemas import ToolListFilters


def get_tool_by_id(db: Session, tool_id: int) -> ToolModel | None:
    return db.query(ToolModel).filter(ToolModel.id == tool_id).first()


def get_tool_by_id_for_owner(db: Session, tool_id: int, owner_id: int) -> ToolModel | None:
    return (
        db.query(ToolModel)
        .filter(ToolModel.id == tool_id, ToolModel.owner_id == owner_id)
        .first()
    )


def list_tools(db: Session, filters: ToolListFilters) -> tuple[list[ToolModel], int]:
    query = db.query(ToolModel).filter(ToolModel.Availability.is_(True))

    if filters.search:
        search_value = f"%{filters.search.strip()}%"
        query = query.filter(
            or_(
                ToolModel.Type.ilike(search_value),
                ToolModel.Brand.ilike(search_value),
                ToolModel.Description.ilike(search_value),
            )
        )

    if filters.power_source:
        query = query.filter(ToolModel.PowerSource == filters.power_source)

    if filters.availability is not None:
        query = query.filter(ToolModel.Availability == filters.availability)

    if filters.category_id is not None:
        query = query.filter(ToolModel.category_id == filters.category_id)

    total = query.with_entities(func.count(ToolModel.id)).scalar() or 0

    if filters.sort == "price_asc":
        query = query.order_by(ToolModel.RatePerDay.asc(), ToolModel.id.desc())
    elif filters.sort == "price_desc":
        query = query.order_by(ToolModel.RatePerDay.desc(), ToolModel.id.desc())
    elif filters.sort == "name":
        query = query.order_by(ToolModel.Type.asc(), ToolModel.id.desc())
    else:
        query = query.order_by(ToolModel.id.desc())

    offset = (filters.page - 1) * filters.page_size
    items = query.offset(offset).limit(filters.page_size).all()
    return items, total


def list_categories(db: Session) -> list[CategoryModel]:
    return db.query(CategoryModel).all()


def list_tools_for_owner(db: Session, owner_id: int) -> list[ToolModel]:
    return (
        db.query(ToolModel)
        .filter(ToolModel.owner_id == owner_id)
        .order_by(ToolModel.id.desc())
        .all()
    )
