from enum import Enum

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

from typing import List
from pydantic import BaseModel


class ToolBase(BaseModel):
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
    owner_id: Optional[int] = None


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
    owner_id: int


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
