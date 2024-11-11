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

    # получить эту бронь и убедиться что она есть
    new_booking = await db.bookings.add(booking_data)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.user_id == new_booking.user_id
    # а еще можно вот так разом сравнить все параметры
    assert booking.model_dump(exclude={"id"}) == booking_data.model_dump()

    # обновить бронь
    updated_date = date(year=2023, month=12, day=25)
    update_booking_data = BookingAdd(
        user_id=booking.user_id,
        room_id=booking.room_id,
        date_from=date(year=2023, month=12, day=25),
        date_to=updated_date,
        price=100,
    )
    await db.bookings.update(update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.date_from == updated_date

    # удалить бронь
    await db.bookings.delete_data(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
