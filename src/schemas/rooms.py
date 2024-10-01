from pydantic import BaseModel, ConfigDict


class RoomAddRequest(BaseModel):

    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomAdd(BaseModel):

    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPATCH(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
