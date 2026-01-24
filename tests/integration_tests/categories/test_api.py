import pytest


@pytest.mark.parametrize(
    "title, status_code",
    [
        pytest.param("Food", 201, id="valid_category"),
        pytest.param("", 422, id="empty_title"),
    ]
)
async def test_post_category(ac, user, title, status_code):
    response = await ac.post("/categories/", json={
        "title": title,
        "user_id": user["id"]
    })

    assert response.status_code == status_code

    if status_code == 201:
        body = response.json()
        assert body["title"] == title
        assert body["user_id"] == user["id"]


async def test_get_category(ac, category):
    response = await ac.get(f"/categories/{category['id']}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_get_categories_by_user(ac, user):
    await ac.post("/categories/", json={"title": "Food", "user_id": user["id"]})
    await ac.post("/categories/", json={"title": "Transport", "user_id": user["id"]})

    response = await ac.get(
        "/categories/",
        params={
            "user_id": user["id"],
            "page": 1,
            "size": 10
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2
    assert {c["title"] for c in data} == {"Food", "Transport"}


async def test_update_category(ac, category):
    response = await ac.patch(
        "/categories/",
        params={"category_id": category["id"]},
        json={"title": "Updated Food"}
    )

    assert response.status_code == 200
    body = response.json()

    assert body["id"] == category["id"]
    assert body["title"] == "Updated Food"


async def test_update_nonexistent_category(ac):
    response = await ac.patch(
        "/categories/",
        params={"category_id": 99999},
        json={"title": "Nope"}
    )

    assert response.status_code == 404


async def test_delete_category(ac, category):
    response = await ac.delete(
        "/categories/",
        params={"category_id": category["id"]}
    )

    assert response.status_code == 200
    assert response.json()["id"] == category["id"]

    get_response = await ac.get(f"/categories/{category['id']}")
    data = get_response.json()
    assert get_response.status_code == 200
    assert data["visible"] == False
