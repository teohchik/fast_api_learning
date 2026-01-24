from datetime import datetime
import pytest


@pytest.mark.parametrize("user_id, category_id, amount, description, status_code", [
    pytest.param(1, 1, 3.75, "Grocery shopping", 201, id="valid_expense"),
    pytest.param(999, 1, 450.75, "Grocery store", 409, id="nonexistent_user"),
    pytest.param(2, 999, 300.00, "Electronics", 409, id="nonexistent_category"),
])
async def test_post_expense(user_id, category_id, amount, description, status_code, ac):
    data = {
        "user_id": user_id,
        "category_id": category_id,
        "amount": amount,
        "description": description
    }
    response = await ac.post(url="/expenses/", json=data)
    assert response.status_code == status_code


async def test_get_expenses_by_user(ac, user, expense):
    now = datetime.now()
    month = now.month
    year = now.year

    response = await ac.get(
        f"/expenses/user/{user['id']}",
        params={"year": year, "month": month}
    )
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    assert data[0]["user_id"] == user["id"]
    assert "amount" in data[0]
    assert "category_id" in data[0]

async def test_get_expense(ac, expense):
    response = await ac.get(f"/expenses/{expense['id']}")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == expense["id"]
    assert data["user_id"] == expense["user_id"]
    assert data["amount"] == expense["amount"]

async def test_update_expense(ac, expense):
    new_amount = expense["amount"] + 10.0
    response = await ac.patch(
        f"/expenses/",
        params={"expense_id": expense["id"]},
        json={"amount": new_amount}
    )
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == expense["id"]
    assert data["amount"] == new_amount

async def test_delete_expense(ac, expense):
    response = await ac.delete(
        f"/expenses/",
        params={"expense_id": expense["id"]}
    )
    assert response.status_code == 204

    get_response = await ac.get(f"/expenses/{expense['id']}")
    assert get_response.status_code == 404