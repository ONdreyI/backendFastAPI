from repositories.base import BaseRepository
from sqlalchemy import func, select, insert
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
        self,
        location,
        title,
        limit,
        offset,
    ):
        query = select(HotelsOrm)
        if location:
            query = query.filter(
                func.lower(HotelsOrm.location).contains(location.strip().lower())
            )
        if title:
            query = query.filter(
                func.lower(HotelsOrm.title).contains(title.strip().lower())
            )
        query = query.limit(limit).offset(offset)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return result.scalars().all()


    async def post_object(
        self,
        hotel_data,
    ):
        query = insert(self.model).values(hotel_data.model_dump())
        result = await self.session.execute(query)
        return result.scalars().all()
