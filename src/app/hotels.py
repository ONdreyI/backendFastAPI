from fastapi import APIRouter, Query, Body
from sqlalchemy import insert, select, or_, func
from src.app.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPUT

from src.database import async_session_maker

from src.models.hotels import HotelsOrm

from src.database import engine

from repositories.hotels import HotelsRepository

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
        location: str | None = Query(None, description="Адрес отлея"),
):

    # per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all()
        # query = select(HotelsOrm)
        # if location:
        #     query = (
        #         query
        #         .filter(func.lower(HotelsOrm.location)
        #                 .contains(location.strip().lower()))
        #     )
        # if title:
        #     query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        # query = (
        #     query
        #     .limit(per_page)
        #     .offset(per_page * (pagination.page - 1))
        # )
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        # result = await session.execute(query)
        #
        # hotels = result.scalars().all()
        # # print(type(hotels), hotels)
        # return hotels


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "deleted"}


@router.post("")
async def create_hotel(
        hotel_data: Hotel = Body(
            openapi_examples={
                "1": {
                    "summary": "Сочи",
                    "value": {
                        "title": "Sochi Hotel",
                        "location": "Sochi citi, Mira st. 5",
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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()


@router.put("/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
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
