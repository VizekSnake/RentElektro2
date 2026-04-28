from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import and_, exists
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.model_utils import apply_update
from app.modules.rentals import repository
from app.modules.rentals.models import Rental as RentalModel
from app.modules.rentals.schemas import (
    AcceptedEnum,
    RentalAdd,
    RentalDecisionUpdate,
    RentalInboxItem,
    RentalInboxTool,
    RentalNotificationsReadResult,
    RentalNotificationsReadUpdate,
    RentalOwnerStatusUpdate,
    RentalParticipant,
    RentalPaymentUpdate,
    RentalUpdate,
)
from app.modules.tools.models import Tool as ToolModel


def _normalize_rental_status(status: AcceptedEnum | None) -> AcceptedEnum:
    return status or AcceptedEnum.not_viewed


def _normalize_bool_flag(value: bool | int | None) -> bool:
    return bool(value)


PENDING_OWNER_STATUSES = {AcceptedEnum.not_viewed, AcceptedEnum.viewed}


def _serialize_rental_feed_item(
    rental: RentalModel,
    tool: ToolModel,
    requester,
    owner,
) -> RentalInboxItem:
    return RentalInboxItem(
        id=rental.id,
        tool_id=rental.tool_id,
        user_id=rental.user_id,
        start_date=rental.start_date.date(),
        end_date=rental.end_date.date(),
        comment=rental.comment,
        owner_comment=rental.owner_comment,
        status=_normalize_rental_status(rental.status),
        is_paid=_normalize_bool_flag(rental.is_paid),
        paid_at=rental.paid_at,
        handed_over_at=rental.handed_over_at,
        returned_at=rental.returned_at,
        renter_seen_at=rental.renter_seen_at,
        tool=RentalInboxTool.model_validate(tool, from_attributes=True),
        requester=RentalParticipant.model_validate(requester, from_attributes=True),
        owner=RentalParticipant.model_validate(owner, from_attributes=True),
    )


def create_rental(db: Session, rental: RentalAdd, current_user_id: int) -> RentalModel:
    if rental.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can create rentals only for yourself.",
        )

    tool = db.query(ToolModel).filter(ToolModel.id == rental.tool_id).first()
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")

    if tool.owner_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot rent your own tool.",
        )

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

    db_rental = RentalModel(
        **rental.model_dump(),
        status=AcceptedEnum.not_viewed,
    )
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


def get_owned_rental_or_404(db: Session, rental_id: int, owner_id: int) -> RentalModel:
    rental = repository.get_by_id_for_owner(db, rental_id, owner_id)
    if rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental


def get_renter_rental_or_404(db: Session, rental_id: int, renter_id: int) -> RentalModel:
    rental = repository.get_by_id_for_renter(db, rental_id, renter_id)
    if rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental


def update_rental(db: Session, rental_id: int, rental_update: RentalUpdate) -> RentalModel:
    db_rental = get_rental_or_404(db, rental_id)
    apply_update(db_rental, rental_update)
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


def list_owner_inbox(db: Session, owner_id: int) -> list[RentalInboxItem]:
    rows = repository.list_for_owner(db, owner_id)
    return [
        _serialize_rental_feed_item(rental, tool, requester, owner)
        for rental, tool, requester, owner in rows
    ]


def list_renter_requests(db: Session, renter_id: int) -> list[RentalInboxItem]:
    rows = repository.list_for_renter(db, renter_id)
    return [
        _serialize_rental_feed_item(rental, tool, requester, owner)
        for rental, tool, requester, owner in rows
    ]


def decide_rental(
    db: Session, rental_id: int, owner_id: int, decision: RentalDecisionUpdate
) -> RentalModel:
    if decision.status not in {AcceptedEnum.accepted, AcceptedEnum.rejected_by_owner}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only accept or reject decisions are allowed here.",
        )

    rental = get_owned_rental_or_404(db, rental_id, owner_id)
    current_status = _normalize_rental_status(rental.status)
    if current_status not in PENDING_OWNER_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This rental request has already been processed.",
        )
    rental.status = decision.status
    rental.owner_comment = decision.owner_comment
    rental.renter_seen_at = None
    if decision.status == AcceptedEnum.rejected_by_owner:
        rental.is_paid = False
        rental.paid_at = None
        rental.handed_over_at = None
        rental.returned_at = None
    try:
        db.commit()
        db.refresh(rental)
        return rental
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc


def pay_rental(
    db: Session,
    rental_id: int,
    renter_id: int,
    payment: RentalPaymentUpdate,
) -> RentalModel:
    if not all(
        [
            payment.cardholder.strip(),
            payment.card_number.strip(),
            payment.expiry_date.strip(),
            payment.cvc.strip(),
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment details are required.",
        )

    rental = get_renter_rental_or_404(db, rental_id, renter_id)
    current_status = _normalize_rental_status(rental.status)
    if current_status != AcceptedEnum.accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only accepted rentals can be paid.",
        )

    rental.is_paid = True
    rental.paid_at = datetime.now(UTC).replace(tzinfo=None)
    rental.status = AcceptedEnum.paid_not_rented
    rental.renter_seen_at = None
    try:
        db.commit()
        db.refresh(rental)
        return rental
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc


def update_owner_rental_status(
    db: Session,
    rental_id: int,
    owner_id: int,
    status_update: RentalOwnerStatusUpdate,
) -> RentalModel:
    allowed_transitions = {
        AcceptedEnum.paid_not_rented: AcceptedEnum.paid_rented,
        AcceptedEnum.paid_rented: AcceptedEnum.fulfilled,
    }

    rental = get_owned_rental_or_404(db, rental_id, owner_id)
    current_status = _normalize_rental_status(rental.status)
    target_status = status_update.status

    if allowed_transitions.get(current_status) != target_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This rental cannot be moved to the requested status.",
        )

    if target_status == AcceptedEnum.paid_rented:
        rental.handed_over_at = datetime.now(UTC).replace(tzinfo=None)
    if target_status == AcceptedEnum.fulfilled:
        rental.returned_at = datetime.now(UTC).replace(tzinfo=None)
    rental.status = target_status
    rental.renter_seen_at = None
    try:
        db.commit()
        db.refresh(rental)
        return rental
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc


def mark_notifications_read(
    db: Session,
    user_id: int,
    payload: RentalNotificationsReadUpdate,
) -> RentalNotificationsReadResult:
    updated_owner = 0
    updated_renter = 0
    now = datetime.now(UTC).replace(tzinfo=None)

    if payload.scope in {"owner", "all"}:
        owner_rows = (
            db.query(RentalModel)
            .join(ToolModel, ToolModel.id == RentalModel.tool_id)
            .filter(ToolModel.owner_id == user_id, RentalModel.status == AcceptedEnum.not_viewed)
            .all()
        )
        for rental in owner_rows:
            rental.status = AcceptedEnum.viewed
        updated_owner = len(owner_rows)

    if payload.scope in {"renter", "all"}:
        renter_rows = db.query(RentalModel).filter(RentalModel.user_id == user_id).all()
        unread_renter_rows = [
            rental
            for rental in renter_rows
            if _normalize_rental_status(rental.status) not in PENDING_OWNER_STATUSES
            and rental.renter_seen_at is None
        ]
        for rental in unread_renter_rows:
            rental.renter_seen_at = now
        updated_renter = len(unread_renter_rows)

    try:
        db.commit()
        return RentalNotificationsReadResult(
            scope=payload.scope,
            updated_owner=updated_owner,
            updated_renter=updated_renter,
        )
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc
