from fastapi import APIRouter, Query, Body
from backendCourse.src.app.dependencies import PaginationDep
from backendCourse.src.schemas.rooms import Room, RoomAdd, RoomPatch, RoomPatchRequest

from backendCourse.src.database import async_session_maker

from backendCourse.src.repositories.rooms import RoomsRepository


router = APIRouter(
    prefix="/hotels",
    tags=["Номера"],
)


@router.get("/{hotel_id}/rooms", name="Получение списка номеров при отеле")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", name="Получение одного отеля")
async def get_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.post("/{hotel_id}/rooms", name="Add room data")
async def create_room(
    hotel_id: int,
    room_data: RoomAdd = Body(
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
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

    return {"status": "Ok", "data": room}


#
#
@router.put("/{hotel_id}/rooms/{room_id}")
async def put_hotel(hotel_id: int, room_id: int, room_data: RoomAdd):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).update(
            id=room_id,
            data=_room_data,
        )
        await session.commit()
        return {"status": "updated"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номерах",
    description="<h1>Можно изменить только часть полей номера</h1>",
)
async def patch_hotel(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(
        hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
    )
    async with async_session_maker() as session:
        await RoomsRepository(session).update(
            id=room_id, data=_room_data, exclude_unset=True, hotel_id=hotel_id
        )
        await session.commit()
        return {"status": "updated"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete_data(id=room_id, hotel_id=hotel_id)
        await session.commit()
        return {"status": "deleted"}
