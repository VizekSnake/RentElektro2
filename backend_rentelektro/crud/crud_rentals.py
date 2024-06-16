from typing import Union, Optional, List

from core.schemas.rentals import RentalAdd, Rental, RentalUpdate
from core.models import Rental as RentalModel
from sqlalchemy import and_, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from core.schemas.rentals import AcceptedEnum


async def create_rental(
    db: Session, rental: RentalAdd
) -> Union[RentalModel, HTTPException]:
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
            status_code=400, detail="The tool is already rented for the given period."
        )

    db_rental = RentalModel(**rental.model_dump())
    db.add(db_rental)
    try:
        db.commit()
        db.refresh(db_rental)
        return db_rental
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error while creating rental {e}")


async def get_rental(db: Session, rental_id: int) -> Optional[RentalModel]:
    rental = db.get(RentalModel, rental_id)
    return rental


async def update_rental(
    db: Session, rental_id: int, rental: RentalUpdate
) -> Optional[RentalModel]:
    db_rental = await get_rental(db, rental_id)
    if not db_rental:
        raise HTTPException(404, "The rental does not exist. Error during update")
    for key, value in vars(rental).items():
        if value is not None:
            setattr(db_rental, key, value)
    db.add(db_rental)
    try:
        db.commit()
        db.refresh(db_rental)
        return db_rental
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def delete_rental(db: Session, rental_id: int) -> None:
    db_rental = await get_rental(db, rental_id)
    if not db_rental:
        raise HTTPException(404, "The rental does not exist. Error")
    try:
        db.delete(db_rental)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(500, "Error while deleting rental")
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


async def get_all_rentals(db: Session) -> List[RentalModel]:
    rentals = db.query(RentalModel).all()
    return rentals
