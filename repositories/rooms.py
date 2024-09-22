from base import BaseRepository
from src.models.rooms import RoomsOrm


class HotelsRepository(BaseRepository):
    model = RoomsOrm
