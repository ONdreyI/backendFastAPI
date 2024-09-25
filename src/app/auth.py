from fastapi import APIRouter

from backendCourse.repositories.users import UsersRepository
from backendCourse.src.database import async_session_maker
from backendCourse.src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = "nlo3497pahfp437dsp"
    new_user_deta = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_deta)
        await session.commit()

    return {"status": "available"}
