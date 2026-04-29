import uuid

from app.core.security import get_current_user
from app.modules.rentals.models import AcceptedEnum as RentalStatus
from app.modules.tools.models import Category as CategoryModel, Tool as ToolModel
from app.modules.users.schemas import UserCreate
from app.modules.users.service import create_user


def _create_tool(db_session, owner_id: uuid.UUID) -> ToolModel:
    category = CategoryModel(
        name="Construction", description="Construction tools", active=True, creator_id=owner_id
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    tool = ToolModel(
        Type="hammer",
        PowerSource="manual",
        Brand="Stanley",
        Description="Heavy-duty hammer",
        category_id=category.id,
        Availability=True,
        Insurance=False,
        Power=0,
        Age=1,
        RatePerDay=15.0,
        ImageURL="https://example.com/hammer.png",
        owner_id=owner_id,
    )
    db_session.add(tool)
    db_session.commit()
    db_session.refresh(tool)
    return tool


def test_rental_crud_flow(auth_client, db_session, test_user):
    owner = create_user(
        db_session,
        UserCreate(
            email="owner@example.com",
            username="owner1",
            password="testpassword",
            firstname="Anna",
            lastname="Owner",
            phone="555000222",
            company=False,
        ),
    )
    tool = _create_tool(db_session, owner_id=owner.id)

    create_response = auth_client.post(
        "/api/v1/rentals",
        json={
            "tool_id": str(tool.id),
            "user_id": str(test_user.id),
            "start_date": "23.03.2026",
            "end_date": "25.03.2026",
            "comment": "Need it for a renovation",
        },
    )

    assert create_response.status_code == 201
    rental_id = create_response.json()["id"]
    assert create_response.json()["status"] == "not_viewed"

    read_response = auth_client.get(f"/api/v1/rentals/{rental_id}")
    assert read_response.status_code == 200
    assert read_response.json()["tool_id"] == str(tool.id)

    update_response = auth_client.patch(
        f"/api/v1/rentals/{rental_id}",
        json={"comment": "Updated comment"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["comment"] == "Updated comment"

    all_response = auth_client.get("/api/v1/rentals")
    assert all_response.status_code == 200
    assert len(all_response.json()) == 1

    delete_response = auth_client.delete(f"/api/v1/rentals/{rental_id}")
    assert delete_response.status_code == 204


def test_owner_inbox_and_decision_flow(auth_client, client, db_session, test_user):
    owner = test_user
    renter = create_user(
        db_session,
        UserCreate(
            email="renter@example.com",
            username="renter1",
            password="testpassword",
            firstname="Jan",
            lastname="Najemca",
            phone="555000111",
            company=False,
        ),
    )
    tool = _create_tool(db_session, owner_id=owner.id)

    create_response = client.post(
        "/api/v1/rentals",
        json={
            "tool_id": str(tool.id),
            "user_id": str(renter.id),
            "start_date": "23.03.2026",
            "end_date": "25.03.2026",
            "comment": "Potrzebuję na weekendowy remont",
        },
    )
    assert create_response.status_code == 403

    app = auth_client.app
    app.dependency_overrides[get_current_user] = lambda: renter
    try:
        create_response = auth_client.post(
            "/api/v1/rentals",
            json={
                "tool_id": str(tool.id),
                "user_id": str(renter.id),
                "start_date": "23.03.2026",
                "end_date": "25.03.2026",
                "comment": "Potrzebuję na weekendowy remont",
            },
        )
        assert create_response.status_code == 201
        rental_id = create_response.json()["id"]
    finally:
        app.dependency_overrides[get_current_user] = lambda: owner

    inbox_response = auth_client.get("/api/v1/rentals/inbox")
    assert inbox_response.status_code == 200
    assert len(inbox_response.json()) == 1
    assert inbox_response.json()[0]["requester"]["username"] == "renter1"
    assert inbox_response.json()[0]["owner"]["username"] == owner.username
    assert inbox_response.json()[0]["tool"]["Brand"] == "Stanley"

    decision_response = auth_client.patch(
        f"/api/v1/rentals/{rental_id}/decision",
        json={"status": "accepted", "owner_comment": "Możesz odebrać jutro po 17:00"},
    )
    assert decision_response.status_code == 200
    assert decision_response.json()["status"] == RentalStatus.accepted.value

    second_decision_response = auth_client.patch(
        f"/api/v1/rentals/{rental_id}/decision",
        json={"status": "rejected_by_owner", "owner_comment": "Za późno"},
    )
    assert second_decision_response.status_code == 400

    app.dependency_overrides[get_current_user] = lambda: renter
    try:
        my_rentals_response = auth_client.get("/api/v1/rentals/my")
        assert my_rentals_response.status_code == 200
        assert len(my_rentals_response.json()) == 1
        assert my_rentals_response.json()[0]["owner"]["username"] == owner.username
        assert my_rentals_response.json()[0]["status"] == RentalStatus.accepted.value

        pay_response = auth_client.patch(
            f"/api/v1/rentals/{rental_id}/pay",
            json={
                "cardholder": "Jan Najemca",
                "card_number": "4242424242424242",
                "expiry_date": "12/30",
                "cvc": "123",
            },
        )
        assert pay_response.status_code == 200
        assert pay_response.json()["status"] == RentalStatus.paid_not_rented.value
    finally:
        app.dependency_overrides[get_current_user] = lambda: owner

    pickup_response = auth_client.patch(
        f"/api/v1/rentals/{rental_id}/owner-status",
        json={"status": "paid_rented"},
    )
    assert pickup_response.status_code == 200
    assert pickup_response.json()["status"] == RentalStatus.paid_rented.value

    return_response = auth_client.patch(
        f"/api/v1/rentals/{rental_id}/owner-status",
        json={"status": "fulfilled"},
    )
    assert return_response.status_code == 200
    assert return_response.json()["status"] == RentalStatus.fulfilled.value
