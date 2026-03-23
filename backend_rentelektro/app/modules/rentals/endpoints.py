from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.modules.rentals import service as rentals_service
from app.core.dependencies import get_db
from app.modules.rentals.schemas import Rental, RentalAdd, RentalUpdate

router = APIRouter(prefix="/rental", tags=["rentals"])


@router.post("/add", response_model=Rental, status_code=201)
async def add_rental(rental: RentalAdd, db: Session = Depends(get_db)):
    return rentals_service.create_rental(db, rental)


@router.get("/read/{rental_id}", response_model=Rental)
async def read_rental(rental_id: int, db: Session = Depends(get_db)):
    return rentals_service.get_rental_or_404(db, rental_id)


@router.patch("/update/{rental_id}", response_model=Rental)
async def update_rental_endpoint(
    rental_id: int, rental: RentalUpdate, db: Session = Depends(get_db)
):
    return rentals_service.update_rental(db, rental_id, rental)


@router.patch("/return/{rental_id}", response_model=Rental)
async def return_rental_endpoint(
    rental_id: int, rental: RentalUpdate, db: Session = Depends(get_db)
):
    return rentals_service.update_rental(db, rental_id, rental)


@router.delete("/delete/{rental_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rental_endpoint(rental_id: int, db: Session = Depends(get_db)):
    rentals_service.delete_rental(db, rental_id)


@router.get("/all", response_model=list[Rental])
async def get_all_rentals_endpoint(db: Session = Depends(get_db)):
    return rentals_service.list_rentals(db)
