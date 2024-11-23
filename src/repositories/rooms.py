from datetime import date

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.exceptions import ObjectNotFoundException, NoFreeRoomsException
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import (
    RoomDataMapper,
    RoomDataWithRelsMapper,
)
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_or_none_with_facilities(
        self,
        room_id,
        hotel_id,
    ):
        query = (
            select(RoomsOrm)
            .options(joinedload(RoomsOrm.facilities))
            .filter(RoomsOrm.id == room_id, RoomsOrm.hotel_id == hotel_id)
        )
        result = await self.session.execute(query)

        room = result.unique().scalars().first()
        if room:
            room = RoomDataWithRelsMapper.map_to_domain_entity(room)

            return room
        else:
            return {"Такого номера не существует"}
