from enum import Enum

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from typing import List
from pydantic import BaseModel


class ToolBase(BaseModel):
    Type: str
    PowerSource: str
    Brand: str
    Description: str
    CategoryID: int
    Availability: bool
    Insurance: bool
    Power: int
    Age: float
    RatePerDay: float
    ImageURL: str


class ToolUpdate(BaseModel):
    Type: Optional[str] = None
    PowerSource: Optional[str] = None
    Brand: Optional[str] = None
    Description: Optional[str] = None
    CategoryID: Optional[int] = None
    Availability: Optional[bool] = None
    Insurance: Optional[bool] = None
    Power: Optional[int] = None
    Age: Optional[float] = None
    RatePerDay: Optional[float] = None
    ImageURL: Optional[str] = None


class ToolAdd(ToolBase):
    pass


class Tool(ToolBase):
    id: int

    class Config:
        from_attributes = True


class TypeEnum(str, Enum):
    hammer = "hammer"
    saw = "saw"
    drill = "drill"


class PowerSourceEnum(str, Enum):
    electric = "electric"
    gas = "gas"
