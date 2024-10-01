from pydantic import Field, BaseModel, ConfigDict


class RoomAdd(BaseModel):

    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPATCH(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)
