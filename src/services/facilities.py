from src.schemas.facilities import FacilitiesAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilitiesService(BaseService):
    async def create_facilities(self, facilities_data: FacilitiesAdd):
        facility = await self.db.facilities.add(facilities_data)
        await self.db.commit()

        test_task.delay()  # type ignore
        return facility
