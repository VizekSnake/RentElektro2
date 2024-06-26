from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from tools.models import Tool as ToolModel, Category as CategoryModel
from tools.schemas import ToolAdd, ToolUpdate, Tool, CategoryAdd, Category


def get_tool(db: Session, tool_id: int):
    return db.query(ToolModel).filter(ToolModel.id == tool_id).first()


def get_all_tools(db: Session) -> List[Tool]:
    return db.query(ToolModel).all()


def get_all_categories(db: Session) -> List[Category]:
    return db.query(CategoryModel).all()


from sqlalchemy.exc import IntegrityError


def create_tool(db: Session, tool: ToolAdd, user_id: int):
    try:
        db_tool = ToolModel(**tool.dict(exclude={"owner_id"}), owner_id=user_id)
        db.add(db_tool)
        db.commit()
        db.refresh(db_tool)
        return db_tool

    except IntegrityError as e:
        db.rollback()
        error_message = f"Error adding tool: {str(e)}"
        raise ValueError(error_message)


def delete_tool(db: Session, tool_id: int):
    db_tool = get_tool(db, tool_id)
    if not db_tool:
        return None
    try:
        db.delete(db_tool)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def update_tool(db: Session, tool_id: int, tool: ToolUpdate):
    db_tool = get_tool(db, tool_id)
    if not db_tool:
        return None
    for var, value in vars(tool).items():
        setattr(db_tool, var, value) if value else None
    db.add(db_tool)
    try:
        db.commit()
        db.refresh(db_tool)
        return db_tool
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def create_category(db: Session, category: CategoryAdd, user_id: int):
    try:
        db_category = CategoryModel(**category.dict(), creator_id=user_id)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    except IntegrityError as e:
        db.rollback()
        error_message = f"Error adding tool: {str(e)}"
        raise ValueError(error_message)


