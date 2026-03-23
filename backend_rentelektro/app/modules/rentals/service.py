from fastapi import HTTPException, status
from sqlalchemy import and_, exists
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.modules.rentals import repository
from app.modules.rentals.models import Rental as RentalModel
from app.modules.rentals.schemas import AcceptedEnum, RentalAdd, RentalUpdate


def create_rental(db: Session, rental: RentalAdd) -> RentalModel:
    overlapping_rentals = db.query(
        exists().where(
            and_(
                RentalModel.tool_id == rental.tool_id,
                RentalModel.status == AcceptedEnum.accepted,
                RentalModel.start_date <= rental.end_date,
                RentalModel.end_date >= rental.start_date,
            )
        )
    ).scalar()

    if overlapping_rentals:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The tool is already rented for the given period.",
        )

    db_rental = RentalModel(**rental.model_dump())
    db.add(db_rental)
    try:
        db.commit()
        db.refresh(db_rental)
        return db_rental
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while creating rental",
        ) from exc


def get_rental_or_404(db: Session, rental_id: int) -> RentalModel:
    rental = repository.get_by_id(db, rental_id)
    if rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental


def update_rental(db: Session, rental_id: int, rental_update: RentalUpdate) -> RentalModel:
    db_rental = get_rental_or_404(db, rental_id)
    update_data = rental_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_rental, key, value)
    try:
        db.commit()
        db.refresh(db_rental)
        return db_rental
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc


def delete_rental(db: Session, rental_id: int) -> None:
    db_rental = get_rental_or_404(db, rental_id)
    try:
        db.delete(db_rental)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while deleting rental",
        ) from exc


def list_rentals(db: Session) -> list[RentalModel]:
    return repository.list_all(db)
