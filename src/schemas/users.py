from pydantic import Field, BaseModel, ConfigDict


class UserRequestAdd(BaseModel):
    email: str
    password: str


class UserAdd(BaseModel):
    email: str
    hashed_password: str


class User(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)
