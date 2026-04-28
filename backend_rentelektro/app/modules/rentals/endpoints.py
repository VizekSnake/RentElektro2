from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.modules.rentals import service as rentals_service
from app.modules.rentals.schemas import (
    Rental,
    RentalAdd,
    RentalDecisionUpdate,
    RentalInboxItem,
    RentalNotificationsReadResult,
    RentalNotificationsReadUpdate,
    RentalOwnerStatusUpdate,
    RentalPaymentUpdate,
    RentalUpdate,
)
from app.modules.users.schemas import User

router = APIRouter(prefix="/rentals", tags=["rentals"])


@router.post("", response_model=Rental, status_code=201)
async def add_rental(
    rental: RentalAdd,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return rentals_service.create_rental(db, rental, user.id)


@router.get("", response_model=list[Rental])
async def get_all_rentals_endpoint(db: Session = Depends(get_db)):
    return rentals_service.list_rentals(db)


@router.get("/inbox", response_model=list[RentalInboxItem])
async def get_owner_inbox(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return rentals_service.list_owner_inbox(db, user.id)


@router.get("/my", response_model=list[RentalInboxItem])
async def get_my_rentals(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return rentals_service.list_renter_requests(db, user.id)


@router.patch("/notifications/read", response_model=RentalNotificationsReadResult)
async def mark_rental_notifications_read(
    payload: RentalNotificationsReadUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return rentals_service.mark_notifications_read(db, user.id, payload)


@router.get("/{rental_id}", response_model=Rental)
async def read_rental(rental_id: int, db: Session = Depends(get_db)):
    return rentals_service.get_rental_or_404(db, rental_id)


@router.patch("/{rental_id}", response_model=Rental)
async def update_rental_endpoint(
    rental_id: int, rental: RentalUpdate, db: Session = Depends(get_db)
):
    return rentals_service.update_rental(db, rental_id, rental)


@router.delete("/{rental_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rental_endpoint(rental_id: int, db: Session = Depends(get_db)):
    rentals_service.delete_rental(db, rental_id)


@router.patch("/{rental_id}/decision", response_model=Rental)
async def decide_rental_endpoint(
    rental_id: int,
    decision: RentalDecisionUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return rentals_service.decide_rental(db, rental_id, user.id, decision)


@router.patch("/{rental_id}/pay", response_model=Rental)
async def pay_rental_endpoint(
    rental_id: int,
    payment: RentalPaymentUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return rentals_service.pay_rental(db, rental_id, user.id, payment)


@router.patch("/{rental_id}/owner-status", response_model=Rental)
async def update_owner_rental_status_endpoint(
    rental_id: int,
    status_update: RentalOwnerStatusUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return rentals_service.update_owner_rental_status(db, rental_id, user.id, status_update)
