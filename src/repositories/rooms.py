from datetime import date

from sqlalchemy import insert, func, select
from sqlalchemy.orm import session

from backendCourse.src.database import engine
from backendCourse.src.models.bookings import BookingsOrm
from backendCourse.src.repositories.base import BaseRepository
from backendCourse.src.models.rooms import RoomsOrm
from backendCourse.src.repositories.utils import rooms_ids_for_booking
from backendCourse.src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
