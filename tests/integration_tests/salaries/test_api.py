from datetime import datetime
import pytest


async def test_api_key_missing(ac, user):
    response = await ac.get(url=f"/salaries/user/{user['id']}", headers={"X-API-KEY": "wrong-key"})
    assert response.status_code == 403


async def test_post_missing_description(ac, user):
    data = {
        "user_id": user["id"],
        "amount": 4444,
    }
    response = await ac.post(url="/salaries/", json=data)
    assert response.status_code == 201


@pytest.mark.parametrize(
    "user_id, amount, description, status_code",
    [
        pytest.param(1, 3.75, "Grocery shopping", 201, id="valid_salary"),
        pytest.param(999, 450.75, "Grocery store", 409, id="nonexistent_user"),
        pytest.param(2, -333, "Electronics", 422, id="invalid_amount"),
    ],
)
async def test_post_salary(user_id, amount, description, status_code, ac):
    data = {
        "user_id": user_id,
        "amount": amount,
        "description": description,
    }
    response = await ac.post(url="/salaries/", json=data)
    assert response.status_code == status_code


async def test_get_salaries_by_user(ac, salary):
    now = datetime.now()
    month = now.month
    year = now.year

    response = await ac.get(
        f"/salaries/user/{salary['user_id']}", params={"year": year, "month": month}
    )
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    assert data[0]["user_id"] == salary["user_id"]
    assert "amount" in data[0]


async def test_get_salary(ac, salary):
    response = await ac.get(f"/salaries/{salary['id']}")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == salary["id"]
    assert data["user_id"] == salary["user_id"]
    assert data["amount"] == salary["amount"]


async def test_update_salary(ac, salary):
    new_amount = salary["amount"] + 10.0
    response = await ac.patch(
        "/salaries/", params={"salary_id": salary["id"]}, json={"amount": new_amount}
    )
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == salary["id"]
    assert data["amount"] == new_amount


async def test_delete_salary(ac, salary):
    response = await ac.delete("/salaries/", params={"salary_id": salary["id"]})
    assert response.status_code == 204

    get_response = await ac.get(f"/salaries/{salary['id']}")
    assert get_response.status_code == 404
