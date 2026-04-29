import uuid

from app.modules.tools.models import Tool as ToolModel
from app.modules.users.schemas import UserCreate
from app.modules.users.service import create_user


def create_tool_owner(db_session):
    owner_data = UserCreate(
        email="owner@example.com",
        username="owner_user",
        password="ownerpassword",
        firstname="Owner",
        lastname="User",
        phone="111222333",
        company=False,
    )
    return create_user(db_session, owner_data)


def create_reviewable_tool(db_session, owner_id: uuid.UUID) -> ToolModel:
    tool = ToolModel(
        Type="drill",
        PowerSource="electric",
        Brand="Bosch",
        Description="Cordless drill",
        category_id=None,
        Availability=True,
        Insurance=False,
        Power=650,
        Age=1.5,
        RatePerDay=49.99,
        ImageURL="https://example.com/drill.png",
        owner_id=owner_id,
    )
    db_session.add(tool)
    db_session.commit()
    db_session.refresh(tool)
    return tool


def test_add_review_and_read_summary(auth_client, db_session, test_user):
    owner = create_tool_owner(db_session)
    tool = create_reviewable_tool(db_session, owner.id)

    create_response = auth_client.post(
        "/api/v1/reviews",
        json={
            "tool_id": str(tool.id),
            "rating": 4.5,
            "comment": "Solid and reliable.",
        },
    )

    assert create_response.status_code == 201
    assert create_response.json()["tool_id"] == str(tool.id)
    assert create_response.json()["user_id"] == str(test_user.id)

    summary_response = auth_client.get(f"/api/v1/reviews/{tool.id}")

    assert summary_response.status_code == 200
    assert summary_response.json()["average_rating"] == 4.5
    assert summary_response.json()["total_reviews"] == 1
    assert summary_response.json()["comments"] == ["Solid and reliable."]


def test_add_review_rejects_duplicate_review(auth_client, db_session):
    owner = create_tool_owner(db_session)
    tool = create_reviewable_tool(db_session, owner.id)

    payload = {
        "tool_id": str(tool.id),
        "rating": 5.0,
        "comment": "Excellent.",
    }
    auth_client.post("/api/v1/reviews", json=payload)
    duplicate_response = auth_client.post("/api/v1/reviews", json=payload)

    assert duplicate_response.status_code == 409


def test_add_review_rejects_own_tool(auth_client, db_session, test_user):
    tool = create_reviewable_tool(db_session, test_user.id)

    response = auth_client.post(
        "/api/v1/reviews",
        json={
            "tool_id": str(tool.id),
            "rating": 3.0,
            "comment": "Should not work.",
        },
    )

    assert response.status_code == 400
