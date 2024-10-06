from datetime import date

from fastapi import APIRouter, Query, Body

from backendCourse.src.app.dependencies import DBDep
from backendCourse.src.schemas.facilities import RoomFacilityAdd
from backendCourse.src.schemas.rooms import (
    RoomAdd,
    RoomAddRequest,
    RoomPatch,
    RoomPatchRequest,
)

router = APIRouter(
    prefix="/hotels",
    tags=["Номера"],
)


@router.get("/{hotel_id}/rooms", name="Получение списка номеров при отеле")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


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
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
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
    await db.rooms_facilities.delete_data(room_id=room_id)
    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room_id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
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
    facility_id_to_delete: int,
    new_facility_id: int,
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
    await db.rooms_facilities.delete_data(
        room_id=room_id,
        facility_id=facility_id_to_delete,
    )
    rooms_facilities_data = [
        RoomFacilityAdd(
            room_id=room_id,
            facility_id=new_facility_id,
        )
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
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
