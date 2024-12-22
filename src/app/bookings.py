from fastapi import APIRouter

from src.app.dependencies import DBDep, UserIdDep
from src.exceptions import (
    AllRoomsAreBookedException,
    AllRoomsAreBookedHTTPException,
)
from src.schemas.bookings import (
    BookingAddRequest,
)
from src.services.bookings import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.get("", name="Получение всех бронирований")
async def get_hotel(
    db: DBDep,
):
    return await BookingService(db).get_hotel()


@router.get("/me", name="Получение только своих бронирований")
async def get_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await BookingService(db).get_bookings(user_id=user_id)


@router.post(
    "",
    name="Add booking data",
)
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingAddRequest,
):
    try:
        booking = await BookingService(db).create_booking(
            user_id=user_id, booking_data=booking_data
        )
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking}
