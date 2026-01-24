async def test_post_expense(ac):
    data = {
        "user_id": 1,
        "category_id": 1,
        "amount": 450.75,
        "description": "Grocery shopping"
    }
    response = await ac.post(url="/expenses/", json=data)
    assert response.status_code == 201
    resp_data = response.json()
    assert resp_data["user_id"] == data["user_id"]
    assert isinstance(resp_data, dict)

async def test_get_expenses(ac):
    response = await ac.get(url="/expenses/user/4", params={"year": 2025, "month": 12})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

