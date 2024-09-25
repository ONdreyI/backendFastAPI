from backendCourse.src.schemas.users import User
from base import BaseRepository
from backendCourse.src.models.users import UsersOrm


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User
