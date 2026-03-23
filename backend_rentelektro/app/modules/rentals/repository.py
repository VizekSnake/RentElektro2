from sqlalchemy.orm import Session

from app.modules.rentals.models import Rental as RentalModel


def get_by_id(db: Session, rental_id: int) -> RentalModel | None:
    return db.get(RentalModel, rental_id)


def list_all(db: Session) -> list[RentalModel]:
    return db.query(RentalModel).all()
