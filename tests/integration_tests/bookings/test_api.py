import pytest

from src.database import async_session_maker_null_pool
from src.utils.db_manager import DBManager


@pytest.fixture(scope="function")
async def bookings_on_delete_all(db):
    await db.bookings.delete_all()
    await db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-02", "2024-08-11", 200),
        (1, "2024-08-03", "2024-08-12", 200),
        (1, "2024-08-04", "2024-08-13", 200),
        (1, "2024-08-05", "2024-08-14", 200),
        (1, "2024-08-06", "2024-08-15", 500),
        (1, "2024-08-17", "2024-08-25", 200),
    ],
)
async def test_add_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    db,
    authenticated_ac,
):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    print(f"{response.json()=}")
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    # [
    #     (1, "2025-08-01", "2025-08-10"),
    # ],
    [
        (1, "2025-08-01", "2025-08-10", 200),
        (1, "2025-08-20", "2025-08-30", 200),
    ],
    # [
    #     (1, "2024-08-01", "2024-08-05", 200),
    #     (1, "2024-08-07", "2024-08-09", 200),
    #     (1, "2024-08-10", "2024-08-15", 200),
    # ],
)
async def test_add_get_bookings(
    bookings_on_delete_all,
    room_id,
    date_from,
    date_to,
    status_code,
    db,
    authenticated_ac,
):
    # room_id = (await db.rooms.get_all())[0].id
    await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    response = authenticated_ac.get(
        "/bookings/me",
    )
    assert "data" in response
