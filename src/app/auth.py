from fastapi import APIRouter
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError

from backendCourse.repositories.users import UsersRepository
from backendCourse.src.database import async_session_maker
from backendCourse.src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = pwd_context.hash(data.password)
    new_user_deta = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_deta)
        await session.commit()

    return {"status": "available"}
