from datetime import date

from fastapi import APIRouter, Query, Body, HTTPException
from fastapi_cache.decorator import cache

from src.app.dependencies import PaginationDep, DBDep
from src.exceptions import (
    ObjectNotFoundException,
)
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.services.hotels import HotelService

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("", name="Получение списка отелей по сортировке")
@cache(expire=800)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
    date_from: date = Query(example="2024-11-09"),
    date_to: date = Query(example="2024-11-10"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}", name="Получение одного отеля")
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    try:
        return await HotelService(db).get_hotel_by_id(hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Отель не найден")


@router.post("", name="Add hotel data")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
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
    ),
):
    hotel = await HotelService(db).create_hotel(hotel_data)
    return {"status": "OK", "hotel": hotel}


@router.put("/{hotel_id}")
async def put_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
    db: DBDep,
):
    await HotelService(db).put_hotel(hotel_id, hotel_data)
    return {"status": "updated"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Можно изменить только часть полей отеля</h1>",
)
async def patch_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    await HotelService(db).patch_hotel(
        hotel_id,
        hotel_data,
        exclude_unset=True,
    )
    return {"status": "updated"}


@router.delete("/{hotel_id}")
async def delete_hotel(
    hotel_id: int,
    db: DBDep,
):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "deleted"}
