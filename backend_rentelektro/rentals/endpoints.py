from core.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from rentals.handlers import (create_rental, delete_rental, get_all_rentals,
                              get_rental, update_rental)
from rentals.schemas import Rental, RentalAdd, RentalCollection, RentalUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/rental", tags=["rentals"])


@router.post("/add", response_model=Rental, status_code=201)
async def add_rental(rental: RentalAdd, db: Session = Depends(get_db)):
    try:
        created_rental = await create_rental(db, rental)
        if created_rental:
            return created_rental
        else:
            raise Exception(
                "Failed to retrieve created rental")

    except Exception as e:
        print(f"Error creating rental: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/read/{rental_id}", response_model=Rental)
async def read_rental(rental_id: int, db: Session = Depends(get_db)):
    rental = await get_rental(db, rental_id)
    if rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental


@router.patch("/update/{rental_id}", response_model=Rental)
async def update_rental_endpoint(
    rental_id: int, rental: RentalUpdate, db: Session = Depends(get_db)
):
    updated_rental = await update_rental(db, rental_id, rental)
    if updated_rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return updated_rental


@router.patch("/return/{rental_id}", response_model=Rental)
async def return_rental_endpoint(
    rental_id: int, rental: RentalUpdate, db: Session = Depends(get_db)
):
    updated_rental = await update_rental(db, rental_id, rental)
    if updated_rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return updated_rental


@router.delete("/delete/{rental_id}", response_model=dict)
async def delete_rental_endpoint(rental_id: str, db: Session = Depends(get_db)):
    deleted_count = await delete_rental(db, rental_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Rental not found")
    return {"message": "Rental deleted"}


@router.get("/all", response_model=RentalCollection)
async def get_all_rentals_endpoint(db: Session = Depends(get_db)):
    rentals = await get_all_rentals(db)
    return rentals
