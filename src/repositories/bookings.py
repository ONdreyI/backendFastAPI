from sqlalchemy import insert

from backendCourse.src.repositories.base import BaseRepository
from backendCourse.src.models.bookings import BookingsOrm
from backendCourse.src.schemas.bookings import Booking
from backendCourse.src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper
