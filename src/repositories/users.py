from sqlalchemy import select
from pydantic import EmailStr

from backendCourse.src.schemas.users import User, UserWithHashedPassword
from backendCourse.src.repositories.base import BaseRepository
from backendCourse.src.models.users import UsersOrm


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)
