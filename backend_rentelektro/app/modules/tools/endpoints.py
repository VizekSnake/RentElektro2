from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.modules.tools import service as tools_service
from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.modules.tools.schemas import ToolAdd, ToolUpdate, Tool, CategoryAdd, Category
from app.modules.users.schemas import User
from typing import List

router = APIRouter(prefix="/tool", tags=["tools"])


@router.post("/add", response_model=Tool)
async def add_tool(tool: ToolAdd, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return tools_service.create_tool(db=db, tool=tool, user_id=user.id)


@router.post("/category/add", response_model=Category)
async def add_category(category: CategoryAdd, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return tools_service.create_category(db=db, category=category, user_id=user.id)


@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tool(tool_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tools_service.delete_tool(db=db, tool_id=tool_id, owner_id=user.id)


@router.patch("/update/{tool_id}", response_model=Tool)
async def update_tool(tool_id: int, tool: ToolUpdate, db: Session = Depends(get_db),
                      user: User = Depends(get_current_user)):
    return tools_service.update_tool(db=db, tool_id=tool_id, tool_update=tool, owner_id=user.id)


@router.get("/all", response_model=List[Tool] | None)
async def get_all(db: Session = Depends(get_db)):
    return tools_service.list_tools_or_404(db)


@router.get("/category/all", response_model=List[Category] | None)
async def get_all_category(db: Session = Depends(get_db)):
    return tools_service.list_categories_or_404(db)


@router.get("/{tool_id}", response_model=Tool)
async def get_tool(tool_id: int, db: Session = Depends(get_db)):
    return tools_service.get_tool_or_404(db, tool_id=tool_id)
