import pytest


@pytest.mark.parametrize("telegram_id, username, first_name, last_name, status_code", [
    pytest.param(574958603, "john_doe", "John", "Doe", 201, id="valid_user_1"),
    pytest.param(574958604, "jane_smith", "Jane", "Smith", 201, id="valid_user_2"),
    pytest.param(574958603, "john_doe", "John", "Doe", 409, id="duplicate_telegram_id"),
    pytest.param(574958608, "alikante33ff", None, "Loif", 422, id="missing_first_name"),
])
async def test_post_user(telegram_id, username, first_name, last_name, status_code, ac):
    url = "/users/"
    data = {"telegram_id": telegram_id, "username": username, "first_name": first_name, "last_name": last_name}

    response = await ac.post(url=url, json=data)
    assert response.status_code == status_code


async def test_get_users(ac):
    url = "/users/"
    response = await ac.get(url=url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
    assert "id" in response.json()[0]
    assert "telegram_id" in response.json()[0]


async def test_get_user_by_id(ac):
    user = {
        "telegram_id": 123123123,
        "username": "temp",
        "first_name": "Temp",
        "last_name": "User"
    }

    r = await ac.post("/users/", json=user)
    user_id = r.json()["id"]

    url = f"/users/{user_id}"
    response = await ac.get(url=url)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_update_user(ac):
    response = await ac.post("/users/", json={
        "telegram_id": 888777666,
        "username": "fixture_user",
        "first_name": "Fixture",
        "last_name": "User"
    })
    new_user_id = response.json()["id"]
    response = await ac.patch(f"/users/{new_user_id}",
                              json={
                                  "username": "updated",
                                  "first_name": "User",
                                  "last_name": "User"})
    assert response.status_code == 200
    updated = await ac.get(f"/users/{new_user_id}")
    assert updated.json()["username"] == "updated"
