from core.mongodb import db
from core.schemas.rentals import Rental
from bson import ObjectId

from core.schemas.rentals import RentalCollection


# async def create_rental(rental: Rental):
#     rental_dict = rental.dict(by_alias=True)
#     result = await db.rentals.insert_one(rental_dict)
#     rental.id = result.inserted_id
#     return rental.id

async def create_rental(rental: Rental):
    """
    Creates a new rental object in MongoDB.

    Args:
        rental (Rental): The rental object data to be inserted.

    Returns:
        ObjectId: The ObjectId of the newly created rental document.
    """

    # Convert rental data to a dictionary (excluding the id field)
    rental_dict = rental.dict(exclude_unset=True, exclude={'id'})

    # Generate a new ObjectId for the rental
    rental_dict["_id"] = ObjectId()

    try:
        # Insert the rental data into the "rentals" collection
        result = await db.rentals.insert_one(rental_dict)
        return result.inserted_id

    except Exception as e:
        print(f"Error creating rental: {e}")
        raise  # Re-raise the exception for handling in the endpoint


async def get_rental(rental_id: str):
    rental = await db.rentals.find_one({"_id": ObjectId(rental_id)})
    if rental:
        return Rental(**rental)
    return None


async def update_rental(rental_id: str, rental: Rental):
    rental_dict = rental.dict(by_alias=True, exclude_unset=True)
    await db.rentals.update_one({"_id": ObjectId(rental_id)}, {"$set": rental_dict})
    updated_rental = await get_rental(rental_id)
    return updated_rental


async def delete_rental(rental_id: str):
    result = await db.rentals.delete_one({"_id": ObjectId(rental_id)})
    return result.deleted_count


async def get_all_rentals():
    rentals_cursor = db.rentals.find()
    rentals = await rentals_cursor.to_list(length=None)
    return RentalCollection(rentals=[Rental(**rental) for rental in rentals])
