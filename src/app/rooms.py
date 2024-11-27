from datetime import date

from fastapi import APIRouter, Query, Body, HTTPException

from src.app.dependencies import DBDep
from src.exceptions import (
    ObjectNotFoundException,
    check_date_to_before_date_from,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
)
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import (
    RoomAdd,
    RoomAddRequest,
    RoomPatch,
    RoomPatchRequest,
)
from src.services.rooms import RoomService

router = APIRouter(
    prefix="/hotels",
    tags=["Номера"],
)


@router.get("/{hotel_id}/rooms", name="Получение списка номеров при отеле")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(exampl="2024-11-09"),
    date_to: date = Query(example="2024-11-10"),
):
    return await RoomService(db).get_filtered_by_time(
        hotel_id,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}/rooms/{room_id}", name="Получение одного отеля")
async def get_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms", name="Add room data")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi Hotel",
                "value": {
                    "title": "Sochi Hotel Room",
                    "description": "A luxurious room in Sochi Hotel",
                    "price": 100,
                    "quantity": 5,
                    "facilities_ids": [1, 2, 3, 4, 5],
                },
            },
            "2": {
                "summary": "Dubai Hotel",
                "value": {
                    "title": "Dubai Hotel Room",
                    "description": "A usually room in Dubai Hotel",
                    "price": 60,
                    "quantity": 15,
                    "facilities_ids": [1, 2, 3],
                },
            },
        }
    ),
):
    try:
        room = RoomService(db).create_room(
            hotel_id,
            room_data,
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_hotel(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    await RoomService(db).put_hotel(
        hotel_id,
        room_id,
        room_data,
    )
    return {"status": "updated"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номерах",
    description="<h1>Можно изменить только часть полей номера</h1>",
)
async def patch_hotel(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    await RoomService(db).partially_edit_room(
        hotel_id,
        room_id,
        room_data,
    )
    return {"status": "updated"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_hotel(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    await RoomService(db).delete_room(
        hotel_id,
        room_id,
    )
    return {"status": "deleted"}
