import typing
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models import RoomsOrm


class RoomsFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    room_id: Mapped[int] = mapped_column(
        ForeignKey(
            "rooms.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    )
    facility_id: Mapped[int] = mapped_column(
        ForeignKey(
            "facilities.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    )


class FacilitiesOrm(Base):
    __tablename__ = "facilities"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities",
    )
