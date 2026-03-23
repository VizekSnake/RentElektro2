from tools.models import Category as CategoryModel


def test_add_tool_and_get_tool(auth_client, db_session, test_user):
    category = CategoryModel(name="Power tools", description="Electric tools", active=True, creator_id=test_user.id)
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = auth_client.post(
        "/api/tool/add",
        json={
            "Type": "drill",
            "PowerSource": "electric",
            "Brand": "Bosch",
            "Description": "Cordless drill",
            "category_id": category.id,
            "Availability": True,
            "Insurance": False,
            "Power": 650,
            "Age": 1.5,
            "RatePerDay": 49.99,
            "ImageURL": "https://example.com/drill.png",
        },
    )

    assert response.status_code == 200
    tool_id = response.json()["id"]
    assert response.json()["owner_id"] == test_user.id

    read_response = auth_client.get(f"/api/tool/{tool_id}")

    assert read_response.status_code == 200
    assert read_response.json()["Brand"] == "Bosch"


def test_get_all_tools_returns_created_tools(auth_client, db_session, test_user):
    category = CategoryModel(name="Garden", description="Garden tools", active=True, creator_id=test_user.id)
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    auth_client.post(
        "/api/tool/add",
        json={
            "Type": "saw",
            "PowerSource": "gas",
            "Brand": "Stihl",
            "Description": "Chainsaw",
            "category_id": category.id,
            "Availability": True,
            "Insurance": True,
            "Power": 1200,
            "Age": 2,
            "RatePerDay": 89.0,
            "ImageURL": "https://example.com/saw.png",
        },
    )

    response = auth_client.get("/api/tool/all")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["Type"] == "saw"
