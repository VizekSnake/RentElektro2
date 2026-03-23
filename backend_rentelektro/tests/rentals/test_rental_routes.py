from tools.models import Category as CategoryModel
from tools.models import Tool as ToolModel


def _create_tool(db_session, owner_id: int) -> ToolModel:
    category = CategoryModel(name="Construction", description="Construction tools", active=True, creator_id=owner_id)
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


def test_rental_crud_flow(client, db_session, test_user):
    tool = _create_tool(db_session, owner_id=test_user.id)

    create_response = client.post(
        "/api/rental/add",
        json={
            "tool_id": tool.id,
            "user_id": test_user.id,
            "start_date": "23.03.2026",
            "end_date": "25.03.2026",
            "comment": "Need it for a renovation",
        },
    )

    assert create_response.status_code == 201
    rental_id = create_response.json()["id"]

    read_response = client.get(f"/api/rental/read/{rental_id}")
    assert read_response.status_code == 200
    assert read_response.json()["tool_id"] == tool.id

    update_response = client.patch(
        f"/api/rental/update/{rental_id}",
        json={"comment": "Updated comment"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["comment"] == "Updated comment"

    all_response = client.get("/api/rental/all")
    assert all_response.status_code == 200
    assert len(all_response.json()) == 1

    delete_response = client.delete(f"/api/rental/delete/{rental_id}")
    assert delete_response.status_code == 204
