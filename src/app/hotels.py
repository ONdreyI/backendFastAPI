from fastapi import APIRouter, Query, Body
from sqlalchemy import insert, select, or_, func
from backendCourse.src.app.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPUT

from src.database import async_session_maker

from src.models.hotels import HotelsOrm

from src.database import engine

from backendCourse.repositories.hotels import HotelsRepository

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location,
            title,
            limit=per_page or 5,
            offset=per_page * (pagination.page - 1),
        )


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete_data(id=hotel_id)
        await session.commit()
        return {"status": "deleted"}


@router.post("")
async def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Sochi Hotel",
                    "location": "Sochi city, Mira st. 5",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Dubai Hotel",
                    "location": "Sheikh Zayed Road Dubai, United Arab Emirates",
                },
            },
        }
    )
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "Ok", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        if hotel_id:
            await HotelsRepository(session).update(id=hotel_id, data=hotel_data)
            await session.commit()
            return {"status": "updated"}
    return {"status": "hotel not found"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Можно изменить только часть полей отеля</h1>",
)
def patch_hotel(hotel_id: int, hotel_data: HotelPUT):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            return {"status": "updated"}
        if hotel["id"] == hotel_id:
            hotel["name"] = hotel_data.name
            return {"status": "updated"}
    return {"status": "hotel not found"}
