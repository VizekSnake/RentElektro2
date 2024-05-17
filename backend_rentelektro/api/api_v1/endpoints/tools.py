from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import get_db
from crud import crud_tool
from core.security import get_current_user
from core.schemas.tools import ToolAdd, ToolUpdate, Tool
from core.schemas.users import User
from typing import List
router = APIRouter(prefix="/api/tool", tags=["tools"])

@router.post("/add", response_model=Tool)
async def add_tool(tool: ToolAdd, user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    return crud_tool.add_tool(db=db, tool=tool)


@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tool(tool_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_tool = crud_tool.get_tool(db, tool_id=tool_id)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="tool not found")
    crud_tool.delete_tool(db=db, tool_id=tool_id)
    return {"ok": True}


@router.patch("/update/{tool_id}", response_model=Tool)
async def update_tool(tool_id: int, tool: ToolUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_tool = crud_tool.get_tool(db, tool_id=tool_id)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="tool not found")
    return crud_tool.update_tool(db=db, tool_id=tool_id, tool=tool)


@router.get("/all", response_model=List[Tool] | None)
async def get_all_tools(db: Session = Depends(get_db)):
    tools = crud_tool.get_all(db)
    if tools:
        return tools
    else:
        raise HTTPException(404, "Tools not found")


@router.get("/{tool_id}", response_model=Tool)
async def get_tool(tool_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_tool = crud_tool.get_tool(db, tool_id=tool_id)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return db_tool
