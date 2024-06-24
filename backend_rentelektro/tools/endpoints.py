from typing import List

from core.dependencies import get_db
from core.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from tools.handlers import (create_category, create_tool, get_all_categories,
                            get_all_tools, get_tool, edit_tool)
from tools.schemas import Category, CategoryAdd, Tool, ToolAdd, ToolUpdate
from users.schemas import User

router = APIRouter(prefix="/tool", tags=["tools"])


@router.post("/add", response_model=Tool)
async def add_tool(tool: ToolAdd,
                   user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    return create_tool(db=db, tool=tool, user_id=user.id)


@router.post("/category/add", response_model=Category)
async def add_category(category: CategoryAdd,
                       user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    return create_category(db=db, category=category, user_id=user.id)


@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tool(tool_id: int, user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    db_tool = get_tool(db, tool_id=tool_id)
    if not db_tool:
        raise HTTPException(status_code=404, detail="tool not found")
    delete_tool(db=db, tool_id=tool_id)
    return {"ok": True}


@router.patch("/update/{tool_id}", response_model=Tool)
async def update_tool(tool_id: int, tool: ToolUpdate,
                      db: Session = Depends(get_db),
                      user: User = Depends(get_current_user)):
    db_tool = get_tool(db, tool_id=tool_id, user_id=user.id)
    if not db_tool:
        raise HTTPException(status_code=404, detail="tool not found")
    return edit_tool(db=db, tool_id=tool_id, tool=tool, user_id=user.id)


@router.get("/all", response_model=List[Tool] | None)
async def get_all(db: Session = Depends(get_db)):
    tools = get_all_tools(db)
    if not tools:
        raise HTTPException(404, "Tools not found")
    return tools


@router.get("/category/all", response_model=List[Category] | None)
async def get_all_category(db: Session = Depends(get_db)):
    categories = get_all_categories(db)
    if not categories:
        raise HTTPException(404, "Categories not found")
    return categories


@router.get("/{tool_id}", response_model=Tool)
async def view_tool(tool_id: int, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    db_tool = get_tool(db, tool_id=tool_id)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return db_tool
