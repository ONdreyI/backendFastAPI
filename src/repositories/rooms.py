from datetime import date

from sqlalchemy import insert, func, select
from sqlalchemy.orm import session

from backendCourse.src.database import engine
from backendCourse.src.models.bookings import BookingsOrm
from backendCourse.src.repositories.base import BaseRepository
from backendCourse.src.models.rooms import RoomsOrm
from backendCourse.src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def filter_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: date,
    ):
        """
        with rooms_count as (
                SELECT room_id, count(*) as rooms_booked from bookings
                WHERE date_to >= '2024-07-01' and date_from <= '2024-07-07'
                 GROUP by room_id
        ),
        rooms_left_table as (
                SELECT rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left_table
                from rooms
                LEFT JOIN rooms_count ON rooms.id = rooms_count.room_id
        )
        SELECT * from rooms_left_table
        WHERE rooms_left > 0;
        """
        rooms_count = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_to >= date_to,
                BookingsOrm.date_from <= date_from,
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )
        rooms_left_table = (
            select(
                self.model.id.label("rooms_id"),
                (
                    self.model.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)
                ).label("rooms_left"),
            )
            .select_from(self.model)
            .outerjoin(
                rooms_count,
                self.model.id == rooms_count.c.room_id,
            )
            .cte(name="rooms_left_table")
        )
        query = (select("*").select_from(rooms_left_table)).filter(
            rooms_left_table.c.rooms_left > 0
        )
