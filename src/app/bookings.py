from fastapi import APIRouter, Query, Body
from backendCourse.src.app.dependencies import PaginationDep, DBDep, UserIdDep
from backendCourse.src.schemas.bookings import (
    Booking,
    BookingAdd,
    BookingAddRequest,
    BookingPatch,
    BookingPatchRequest,
)


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.get("", name="Получение всех бронирований")
async def get_hotel(
    db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me", name="Получение только своих бронирований")
async def get_rooms(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post(
    "",
    name="Add booking data",
)
async def create_room(
    db: DBDep,
    user_id: int,
    booking_data: BookingAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi Hotel",
                "value": {
                    "room_id": 4,
                    "date_from": "2024-10-05",
                    "date_to": "2024-10-25",
                    "description": "A luxurious room in Sochi Hotel",
                },
            },
            "2": {
                "summary": "Dubai Hotel",
                "value": {
                    "room_id": 9,
                    "user_id": 8,
                    "date_from": "2024-11-05",
                    "date_to": "2024-11-25",
                    "description": "A luxurious room in Sochi Hotel",
                    "price": 100,
                },
            },
        }
    ),
):
    # Получить схему номера
    # Создать схему данных BookingAdd
    # добавить бронирование конкретному пользователю.
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "Ok", "data": booking}


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
