from sqlalchemy import insert

from backendCourse.src.repositories.base import BaseRepository
from backendCourse.src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from backendCourse.src.schemas.facilities import Facilities, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility
