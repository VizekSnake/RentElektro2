from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.modules.tools import service as tools_service
from app.modules.tools.schemas import (
    Category,
    CategoryAdd,
    PaginatedTools,
    Tool,
    ToolAdd,
    ToolListFilters,
    ToolUpdate,
)
from app.modules.users.schemas import User

router = APIRouter(prefix="/tool", tags=["tools"])


@router.post("/add", response_model=Tool)
async def add_tool(
    tool: ToolAdd, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return tools_service.create_tool(db=db, tool=tool, user_id=user.id)


@router.post("/category/add", response_model=Category)
async def add_category(
    category: CategoryAdd, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return tools_service.create_category(db=db, category=category, user_id=user.id)


@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tool(
    tool_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    tools_service.delete_tool(db=db, tool_id=tool_id, owner_id=user.id)


@router.patch("/update/{tool_id}", response_model=Tool)
async def update_tool(
    tool_id: int,
    tool: ToolUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return tools_service.update_tool(db=db, tool_id=tool_id, tool_update=tool, owner_id=user.id)


@router.get("/all", response_model=PaginatedTools)
async def get_all(
    search: str | None = Query(default=None),
    power_source: str | None = Query(default=None),
    availability: bool | None = Query(default=None),
    category_id: int | None = Query(default=None),
    sort: str = Query(default="newest"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=9, ge=1, le=24),
    db: Session = Depends(get_db),
):
    filters = ToolListFilters(
        search=search,
        power_source=power_source,
        availability=availability,
        category_id=category_id,
        sort=sort,
        page=page,
        page_size=page_size,
    )
    return tools_service.list_tools_or_404(db, filters)


@router.get("/category/all", response_model=List[Category] | None)
async def get_all_category(db: Session = Depends(get_db)):
    return tools_service.list_categories_or_404(db)


@router.get("/mine", response_model=List[Tool])
async def get_my_tools(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return tools_service.list_owner_tools(db, user.id)


@router.get("/{tool_id}", response_model=Tool)
async def get_tool(tool_id: int, db: Session = Depends(get_db)):
    return tools_service.get_tool_or_404(db, tool_id=tool_id)
