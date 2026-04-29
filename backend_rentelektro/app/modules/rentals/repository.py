import uuid
from typing import cast

from sqlalchemy.orm import Session, aliased

from app.modules.rentals.models import Rental as RentalModel
from app.modules.tools.models import Tool as ToolModel
from app.modules.users.models import User as UserModel

RentalFeedRow = tuple[RentalModel, ToolModel, UserModel, UserModel]


def get_by_id(db: Session, rental_id: uuid.UUID) -> RentalModel | None:
    return db.get(RentalModel, rental_id)


def list_all(db: Session) -> list[RentalModel]:
    return db.query(RentalModel).all()


def get_by_id_for_owner(
    db: Session, rental_id: uuid.UUID, owner_id: uuid.UUID
) -> RentalModel | None:
    return (
        db.query(RentalModel)
        .join(ToolModel, ToolModel.id == RentalModel.tool_id)
        .filter(RentalModel.id == rental_id, ToolModel.owner_id == owner_id)
        .first()
    )


def get_by_id_for_renter(
    db: Session, rental_id: uuid.UUID, renter_id: uuid.UUID
) -> RentalModel | None:
    return (
        db.query(RentalModel)
        .filter(RentalModel.id == rental_id, RentalModel.user_id == renter_id)
        .first()
    )


def list_for_owner(db: Session, owner_id: uuid.UUID) -> list[RentalFeedRow]:
    owner = aliased(UserModel)
    requester = aliased(UserModel)
    rows = (
        db.query(RentalModel, ToolModel, requester, owner)
        .join(ToolModel, ToolModel.id == RentalModel.tool_id)
        .join(requester, requester.id == RentalModel.user_id)
        .join(owner, owner.id == ToolModel.owner_id)
        .filter(owner.id == owner_id)
        .order_by(RentalModel.created_at.desc(), RentalModel.id.desc())
        .all()
    )
    return cast(list[RentalFeedRow], rows)


def list_for_renter(db: Session, renter_id: uuid.UUID) -> list[RentalFeedRow]:
    owner = aliased(UserModel)
    requester = aliased(UserModel)
    rows = (
        db.query(RentalModel, ToolModel, requester, owner)
        .join(ToolModel, ToolModel.id == RentalModel.tool_id)
        .join(requester, requester.id == RentalModel.user_id)
        .join(owner, owner.id == ToolModel.owner_id)
        .filter(requester.id == renter_id)
        .order_by(RentalModel.created_at.desc(), RentalModel.id.desc())
        .all()
    )
    return cast(list[RentalFeedRow], rows)
