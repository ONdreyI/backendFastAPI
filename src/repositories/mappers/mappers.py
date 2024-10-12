from backendCourse.src.models.hotels import HotelsOrm
from backendCourse.src.repositories.mappers.base import DataMapper
from backendCourse.src.schemas.hotels import Hotel


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel
