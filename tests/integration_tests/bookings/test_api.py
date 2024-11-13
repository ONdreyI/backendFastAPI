async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    user_id = (await db.users.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "user_id": user_id,
            "date_from": "2023-12-12",
            "date_to": "2024-01-01",
        },
    )
    print(f"{response.json()=}")
    # assert response.status_code == 200
    # res = response.json()
    # assert isinstance(res, dict)
    # assert res["status"] == "OK"
    # assert "data" in res
