# backend/src/models/__init__.py
from .hotels import HotelsOrm
from .rooms import RoomsOrm
from .users import UsersOrm
from .bookings import BookingsOrm
from .facilities import FacilitiesOrm, RoomsFacilitiesOrm

__all__ = [
    "HotelsOrm",
    "RoomsOrm",
    "UsersOrm",
    "BookingsOrm",
    "FacilitiesOrm",
    "RoomsFacilitiesOrm"
]

