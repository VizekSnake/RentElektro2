from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

ToolSort = Literal["newest", "price_asc", "price_desc", "name"]


class ToolBase(BaseModel):
    Type: str
    PowerSource: str
    Brand: str
    Description: str
    category_id: UUID | None = None
    Availability: bool
    Insurance: bool
    Power: int | None = None
    Age: float | None = None
    RatePerDay: float | None = None
    ImageURL: str | None = None


class ToolReadFields(BaseModel):
    TypeLabel: Optional[str] = None
    PowerSourceLabel: Optional[str] = None
    CategoryName: Optional[str] = None


class ToolUpdate(BaseModel):
    Type: Optional[str] = None
    PowerSource: Optional[str] = None
    Brand: Optional[str] = None
    Description: Optional[str] = None
    category_id: Optional[UUID] = None
    Availability: Optional[bool] = None
    Insurance: Optional[bool] = None
    Power: Optional[int] = None
    Age: Optional[float] = None
    RatePerDay: Optional[float] = None
    ImageURL: Optional[str] = None


class ToolAdd(ToolBase):
    owner_id: Optional[UUID] = None


class Tool(ToolBase, ToolReadFields):
    id: UUID
    public_id: str
    owner_id: UUID

    model_config = ConfigDict(from_attributes=True)


class ToolCategory(BaseModel):
    name: str
    description: str
    active: bool

    model_config = ConfigDict(from_attributes=True)


class Category(ToolCategory):
    creator_id: UUID
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class CategoryAdd(ToolCategory):
    pass


class ToolListFilters(BaseModel):
    search: str | None = None
    power_source: str | None = None
    availability: bool | None = None
    category_id: UUID | None = None
    sort: ToolSort = "newest"
    page: int = 1
    page_size: int = 9


class PaginatedTools(BaseModel):
    items: list[Tool]
    total: int
    page: int
    page_size: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)
