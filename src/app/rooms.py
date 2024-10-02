from fastapi import APIRouter, Query, Body
from backendCourse.src.app.dependencies import PaginationDep, DBDep
from backendCourse.src.schemas.rooms import (
    Room,
    RoomAdd,
    RoomAddRequest,
    RoomPatch,
    RoomPatchRequest,
)

from backendCourse.src.database import async_session_maker

from backendCourse.src.repositories.rooms import RoomsRepository


router = APIRouter(
    prefix="/hotels",
    tags=["Номера"],
)


@router.get("/{hotel_id}/rooms", name="Получение списка номеров при отеле")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", name="Получение одного отеля")
async def get_hotel(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    return await db.rooms.get_one_or_none(id=room_id)


@router.post("/{hotel_id}/rooms", name="Add room data")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi Hotel",
                "value": {
                    "hotel_id": 12,
                    "title": "Sochi Hotel Room",
                    "description": "A luxurious room in Sochi Hotel",
                    "price": 100,
                    "quantity": 5,
                },
            },
            "2": {
                "summary": "Dubai Hotel",
                "value": {
                    "hotel_id": 19,
                    "title": "Dubai Hotel Room",
                    "description": "A usually room in Dubai Hotel",
                    "price": 60,
                    "quantity": 15,
                },
            },
        }
    ),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "Ok", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_hotel(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update(
        _room_data,
        id=room_id,
    )
    await db.commit()
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
    _room_data = RoomPatch(
        hotel_id=hotel_id,
        **room_data.model_dump(exclude_unset=True),
    )
    await db.rooms.update(
        _room_data,
        id=room_id,
        exclude_unset=True,
        hotel_id=hotel_id,
    )
    await db.commit()
    return {"status": "updated"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_hotel(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    await db.rooms.delete_data(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "deleted"}
