from sqlalchemy import insert

from backendCourse.src.repositories.base import BaseRepository
from backendCourse.src.models.facilities import FacilitiesOrm
from backendCourse.src.schemas.facilities import Facilities


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities
