from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    description: str | None = None


class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    description: str | None = None
    price: int


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookingPatchRequest(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    description: str | None = None
    price: int | None = None


class BookingPatch(BaseModel):
    room_id: int | None = None
    user_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None
    description: str | None = None
    price: int | None = None
