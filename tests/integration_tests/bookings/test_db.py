from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    booking_data = BookingAdd(
        user_id=(await db.users.get_all())[0].id,
        room_id=(await db.rooms.get_all())[0].id,
        date_from=date(year=2023, month=12, day=12),
        date_to=date(year=2024, month=1, day=1),
        price=100,
    )
    await db.bookings.add(booking_data)
    await db.bookings.get_all(booking_data)
    await db.bookings.update(booking_data)
    await db.bookings.delete_data()

    await db.commit()
