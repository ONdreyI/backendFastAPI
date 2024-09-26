from fastapi import (
    APIRouter,
    HTTPException,
    Response,
    Request,
)

from fastapi import (
    APIRouter,
    HTTPException,
    Response,
    Request,
)

from backendCourse.src.app.dependencies import UserIdDep
from backendCourse.src.database import async_session_maker
from backendCourse.src.repositories.users import UsersRepository
from backendCourse.src.schemas.users import (
    UserRequestAdd,
    UserAdd,
)
from backendCourse.src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = AuthService().pwd_context.hash(data.password)
    new_user_deta = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_deta)
        await session.commit()

    return {"status": "available"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(
            email=data.email
        )
        if not user:
            raise HTTPException(
                status_code=401, detail="Пользователь с таким email не существует"
            )
        if not AuthService().verify_password(
            data.password, hashed_password=user.hashed_password
        ):
            raise HTTPException(status_code=401, detail="Неверный пароль")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie(
            key="access_token",
            value=access_token,
        )
        return {"access_token": access_token}


@router.get("/me")
async def get_me(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return {"user": user}


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "Вы вышли из системы"}
