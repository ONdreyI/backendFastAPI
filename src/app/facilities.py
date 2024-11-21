from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.app.dependencies import DBDep
from src.schemas.facilities import (
    FacilitiesAdd,
)
from src.tasks.tasks import test_task

router = APIRouter(
    prefix="/facilities",
    tags=["Удобства"],
)


@router.get("")
@cache(expire=800)
async def get_facilities(db: DBDep):
    print("ИДУ В БАЗУ ДАННЫХ")
    return await db.facilities.get_all()


# @router.get("", name="Получение одного удобства")
# async def get_hotel(
#     db: DBDep,
#     facilities_id: int,
#     room_id: int,
# ):
#     return await db.facilities.get_one_or_none(id=facilities_id)


@router.post("", name="Добавление удобства")
async def create_room(
    db: DBDep,
    facilities_data: FacilitiesAdd = Body(
        openapi_examples={
            "1": {
                "summary": "WiFi",
                "value": {
                    "title": "WiFi",
                },
            },
            "2": {
                "summary": "Air conditioning",
                "value": {
                    "title": "Air conditioning",
                },
            },
        }
    ),
):

    facility = await db.facilities.add(facilities_data)
    await db.commit()
    test_task.delay()
    return {"status": "Ok", "data": facility}


# @router.put("/{hotel_id}/rooms/{room_id}")
# async def put_hotel(
#     db: DBDep,
#     hotel_id: int,
#     room_id: int,
#     room_data: RoomAddRequest,
# ):
#     _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
#     await db.rooms.update(
#         _room_data,
#         id=room_id,
#     )
#     await db.commit()
#     return {"status": "updated"}


# @router.patch(
#     "/{hotel_id}/rooms/{room_id}",
#     summary="Частичное обновление данных о номерах",
#     description="<h1>Можно изменить только часть полей номера</h1>",
# )
# async def patch_hotel(
#     db: DBDep,
#     hotel_id: int,
#     room_id: int,
#     room_data: RoomPatchRequest,
# ):
#     _room_data = RoomPatch(
#         hotel_id=hotel_id,
#         **room_data.model_dump(exclude_unset=True),
#     )
#     await db.rooms.update(
#         _room_data,
#         id=room_id,
#         exclude_unset=True,
#         hotel_id=hotel_id,
#     )
#     await db.commit()
#     return {"status": "updated"}


# @router.delete("/{hotel_id}/rooms/{room_id}")
# async def delete_hotel(
#     db: DBDep,
#     hotel_id: int,
#     room_id: int,
# ):
#     await db.rooms.delete_data(id=room_id, hotel_id=hotel_id)
#     await db.commit()
#     return {"status": "deleted"}
