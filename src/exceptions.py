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
