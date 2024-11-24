from datetime import date

from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class NoFreeRoomsException(NabronirovalException):
    detail = "Нет свободных номеров"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"


class DateToBeforeDateFrom(NabronirovalException):
    detail = "Дата начала бронирования должна быть раньше даты окончания"


class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Объект уже существует"


def check_date_to_before_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=422, detail="Дата заезда не может быть позже даты выезда"
        )
