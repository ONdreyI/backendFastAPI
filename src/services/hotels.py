from datetime import date

from src.exceptions import check_date_to_before_date_from
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        pagination,
        location: str | None,
        title: str | None,
        date_from: date,
        date_to: date,
    ):
        check_date_to_before_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel_by_id(self, hotel_id: int):
        hotel = await self.db.hotels.get_one(id=hotel_id)
        await self.db.commit()
        return hotel

    async def create_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def put_hotel(
        self,
        hotel_id: int,
        hotel_data: HotelAdd,
    ):
        await self.db.hotels.update(
            id=hotel_id,
            data=hotel_data,
        )
        await self.db.commit()
        return {"status": "updated"}

    async def patch_hotel(
        self,
        hotel_id: int,
        hotel_data: HotelPATCH,
        exclude_unset: bool = False,
    ):
        await self.db.hotels.update(
            id=hotel_id,
            data=hotel_data,
            exclude_unset=exclude_unset,
        )
        await self.db.commit()
        return {"status": "updated"}

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete_data(id=hotel_id)
        await self.db.commit()
