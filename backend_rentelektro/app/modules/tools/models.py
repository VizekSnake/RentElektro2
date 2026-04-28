from __future__ import annotations

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

TOOL_TYPE_LABELS: dict[str, str] = {
    "drill": "Wiertarka",
    "drill_driver": "Wiertarko-wkretarka",
    "grinder": "Szlifierka",
    "saw": "Pila",
    "hammer": "Mlot",
    "rotary_hammer": "Mlot udarowy",
    "driver": "Wkretarka",
    "industrial_vacuum": "Odkurzacz przemyslowy",
    "mower": "Kosiarka",
    "trimmer": "Podkaszarka",
    "pressure_washer": "Myjka cisnieniowa",
    "generator": "Agregat pradotworczy",
    "welder": "Spawarka",
    "compressor": "Kompresor",
    "chainsaw": "Pilarka lancuchowa",
    "circular_saw": "Pilarka tarczowa",
    "jigsaw": "Wyrzynarka",
    "compactor": "Zageszczarka",
    "tiller": "Glebogryzarka",
}

POWER_SOURCE_LABELS: dict[str, str] = {
    "electric": "Elektryczne",
    "gas": "Spalinowe",
}


class Tool(Base):
    __tablename__ = "tools"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    Type: Mapped[str] = mapped_column(String)
    PowerSource: Mapped[str] = mapped_column(String)
    Brand: Mapped[str] = mapped_column(String)
    Description: Mapped[str] = mapped_column(String)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    Availability: Mapped[bool] = mapped_column(Boolean)
    Insurance: Mapped[bool] = mapped_column(Boolean)
    Power: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Age: Mapped[float | None] = mapped_column(Float, nullable=True)
    RatePerDay: Mapped[float | None] = mapped_column(Float, nullable=True)
    ImageURL: Mapped[str | None] = mapped_column(String, nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    category = relationship("Category", back_populates="tools")
    owner = relationship("User", back_populates="tools")

    @property
    def TypeLabel(self) -> str:
        return TOOL_TYPE_LABELS.get(self.Type, self.Type)

    @property
    def PowerSourceLabel(self) -> str:
        return POWER_SOURCE_LABELS.get(self.PowerSource, self.PowerSource)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    tools = relationship("Tool", back_populates="category")
