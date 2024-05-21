from fastapi import APIRouter, HTTPException, Body
from core.schemas.rentals import Rental, RentalAdd, RentalCollection, RentalUpdate
from crud.crud_rentals import create_rental, get_rental, update_rental, delete_rental, get_all_rentals

from core.mongodb import client

router = APIRouter(prefix="/api/rental", tags=["rentals"])


@router.post("/add", response_model=Rental, status_code=201)
async def add_rental(rental: RentalAdd):
    try:
        rental_id = await create_rental(rental)
        created_rental = await get_rental(rental_id)
        if created_rental:

            return created_rental
        else:
            raise Exception("Failed to retrieve created rental")  # Handle unexpected case

    except Exception as e:
        print(f"Error creating rental: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/read/{rental_id}", response_model=Rental)
async def read_rental(rental_id: str):
    rental = await get_rental(rental_id)
    if rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental


@router.patch("/update/{rental_id}", response_model=Rental)
async def update_rental_endpoint(rental_id: str, rental: RentalUpdate):
    updated_rental = await update_rental(rental_id, rental)
    if updated_rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return updated_rental


@router.delete("/delete/{rental_id}", response_model=dict)
async def delete_rental_endpoint(rental_id: str):
    deleted_count = await delete_rental(rental_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Rental not found")
    return {"message": "Rental deleted"}


@router.get("/all", response_model=RentalCollection)
async def get_all_rentals_endpoint():
    rentals = await get_all_rentals()
    return rentals
