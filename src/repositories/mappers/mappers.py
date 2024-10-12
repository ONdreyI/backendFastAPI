from backendCourse.src.models.bookings import BookingsOrm
from backendCourse.src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from backendCourse.src.models.hotels import HotelsOrm
from backendCourse.src.models.rooms import RoomsOrm
from backendCourse.src.models.users import UsersOrm
from backendCourse.src.repositories.mappers.base import DataMapper
from backendCourse.src.schemas.bookings import Booking
from backendCourse.src.schemas.facilities import Facilities, RoomFacility
from backendCourse.src.schemas.hotels import Hotel
from backendCourse.src.schemas.rooms import Room, RoomWithRels
from backendCourse.src.schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facilities


class RoomFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesOrm
    schema = RoomFacility
