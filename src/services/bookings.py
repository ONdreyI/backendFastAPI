from src.app.dependencies import UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.hotels import Hotel
from src.services.base import BaseService
from src.services.rooms import RoomService


class BookingService(BaseService):
    async def get_hotel(
        self,
    ):
        return await self.db.bookings.get_all()

    async def get_bookings(
        self,
        user_id: UserIdDep,
    ):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def create_booking(
        self,
        user_id: UserIdDep,
        booking_data: BookingAddRequest,
    ):
        room = await RoomService(self.db).get_room_with_check(booking_data.room_id)
        hotel: Hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **booking_data.model_dump(),
        )
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        await self.db.commit()
        return booking
