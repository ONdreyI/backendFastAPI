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
