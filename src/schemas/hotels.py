from pydantic import Field, BaseModel


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotel(HotelAdd):
    id: int


class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
