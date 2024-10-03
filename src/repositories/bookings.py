from sqlalchemy import insert

from backendCourse.src.repositories.base import BaseRepository
from backendCourse.src.models.bookings import BookingsOrm
from backendCourse.src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking


