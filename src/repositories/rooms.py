from sqlalchemy import insert

from backendCourse.src.repositories.base import BaseRepository
from backendCourse.src.models.rooms import RoomsOrm
from backendCourse.src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def post_object(
        self,
        room_data,
    ):
        query = insert(self.model).values(room_data.model_dump())
        result = await self.session.execute(query)
        return result.scalars().all()
