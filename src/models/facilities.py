from sqlalchemy import String, ForeignKey, Sequence
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class FacilitiesOrm(Base):
    __tablename__ = "facilities"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))


class RoomsFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        server_default=Sequence("rooms_facilities_id_seq").next_value(),
    )
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
