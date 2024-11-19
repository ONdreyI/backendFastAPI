from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(
        self,
        *filter,
        limit=None,
        offset=None,
        **filter_by,
    ):

        query = select(self.model).filter(*filter).filter_by(**filter_by)
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_all(self, *args):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def update(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ) -> None:
        """
        Update an existing record in the database.
        """
        update_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_data_stmt)

    async def delete_data(self, **filter_by) -> None:
        """
        Delete a record from the database.
        """
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

    async def delete_all(self):
        delete_stmt = delete(self.model)
        await self.session.execute(delete_stmt)
