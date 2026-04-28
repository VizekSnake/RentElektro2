from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ToolBase(BaseModel):
    Type: Optional[str] = None
    TypeLabel: Optional[str] = None
    PowerSource: Optional[str] = None
    PowerSourceLabel: Optional[str] = None
    Brand: Optional[str] = None
    Description: Optional[str] = None
    category_id: Optional[int] = None
    Availability: Optional[bool] = None
    Insurance: Optional[bool] = None
    Power: Optional[int] = None
    Age: Optional[float] = None
    RatePerDay: Optional[float] = None
    ImageURL: Optional[str] = None


class ToolUpdate(BaseModel):
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


class ToolAdd(ToolBase):
    owner_id: Optional[int] = None


class Tool(ToolBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class TypeEnum(str, Enum):
    hammer = "hammer"
    saw = "saw"
    drill = "drill"


class PowerSourceEnum(str, Enum):
    electric = "electric"
    gas = "gas"


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
