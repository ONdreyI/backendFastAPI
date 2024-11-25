async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2023-12-12",
            "date_to": "2024-01-10",
        },
    )
    print(f"{response.json()=}")
    assert response.status_code == 200


async def test_patch_hotels(ac):
    hotel_id = 2  # Replace with the actual hotel ID
    response = await ac.patch(
        f"/hotels/{hotel_id}",
        json={"title": "New Hotel Title"},
    )
    print(f"{response.json()=}")
    assert response.status_code == 200
    # assert response.json().get("title")[0] == "New Hotel Title"


async def test_delete(ac):
    hotel_id = 1  # Replace with the actual hotel ID
    response = await ac.delete(f"/hotels/{hotel_id}")
    assert response.status_code == 200
    assert response.json().get("status") == "deleted"
