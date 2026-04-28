from typing import Optional

from pydantic import BaseModel, ConfigDict


class ToolWriteFields(BaseModel):
    Type: Optional[str] = None
    PowerSource: Optional[str] = None
    Brand: Optional[str] = None
    Description: Optional[str] = None
    category_id: Optional[int] = None
    Availability: Optional[bool] = None
    Insurance: Optional[bool] = None
    Power: Optional[int] = None
    Age: Optional[float] = None
    RatePerDay: Optional[float] = None
    ImageURL: Optional[str] = None


class ToolBase(ToolWriteFields):
    TypeLabel: Optional[str] = None
    PowerSourceLabel: Optional[str] = None


class ToolUpdate(ToolWriteFields):
    pass


class ToolAdd(ToolBase):
    owner_id: Optional[int] = None


class Tool(ToolBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class ToolCategory(BaseModel):
    name: str
    description: str
    active: bool

    model_config = ConfigDict(from_attributes=True)


class Category(ToolCategory):
    creator_id: int
    id: int

    model_config = ConfigDict(from_attributes=True)


class CategoryAdd(ToolCategory):
    pass


class ToolListFilters(BaseModel):
    search: str | None = None
    power_source: str | None = None
    availability: bool | None = None
    category_id: int | None = None
    sort: str = "newest"
    page: int = 1
    page_size: int = 9


class PaginatedTools(BaseModel):
    items: list[Tool]
    total: int
    page: int
    page_size: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)
