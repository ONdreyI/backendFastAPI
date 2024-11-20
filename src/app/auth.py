from fastapi import (
    APIRouter,
    HTTPException,
    Response,
)

from src.app.dependencies import UserIdDep, DBDep
from src.schemas.users import (
    UserRequestAdd,
    UserAdd,
)
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd,
):
    hashed_password = AuthService().pwd_context.hash(data.password)
    new_user_deta = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add(new_user_deta)
    await db.commit()
    return {"status": "available"}


@router.post("/login")
async def login_user(
    db: DBDep,
    data: UserRequestAdd,
    response: Response,
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
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
    return {"access_token": access_token, "status": "OK"}


@router.get("/me")
async def get_me(
    user_id: UserIdDep,
    db: DBDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return {"user": user}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "Вы вышли из системы"}
