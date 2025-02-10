from uuid import UUID, uuid4
from databases import Database
from sqlalchemy import select, and_
from typing import List, Optional
from domain.entities import MeetingRoom
from domain.models import ReservationCreate
from domain.exceptions import (
    RoomNotFoundException,
    ReservationNotFoundException,
    ReservationConflictException,
)
from infrastructure.models import RoomDB, ReservationDB
from domain.observers.observer import (
    ReservationSubject,
    LoggingObserver,
    EmailObserver,
)


class RoomRepository:
    def __init__(self, database: Database):
        self.db = database
        self.reservation_subject = ReservationSubject()
        self.reservation_subject.attach(LoggingObserver())
        self.reservation_subject.attach(EmailObserver())

    async def add(self, room: MeetingRoom) -> None:
        query = RoomDB.__table__.insert().values(
            id=str(room.id),
            name=room.name,
            capacity=room.capacity,
            location=room.location,
        )
        await self.db.execute(query)

    async def get(self, room_id: UUID) -> MeetingRoom:
        query = select(RoomDB).where(RoomDB.id == str(room_id))
        room_db = await self.db.fetch_one(query)

        if not room_db:
            raise RoomNotFoundException(f"Sala com id {room_id} não encontrada")

        reservations_query = select(ReservationDB).where(
            ReservationDB.room_id == str(room_id)
        )
        reservations_db = await self.db.fetch_all(reservations_query)

        reservations = [
            {
                "id": res.id,
                "user_id": res.user_id,
                "start_time": res.start_time,
                "end_time": res.end_time,
            }
            for res in reservations_db
        ]

        return MeetingRoom.from_db(room_db, reservations)

    async def get_all(self) -> List[MeetingRoom]:
        query = select(RoomDB)
        rooms_db = await self.db.fetch_all(query)

        rooms = []
        for room_db in rooms_db:
            reservations_query = select(ReservationDB).where(
                ReservationDB.room_id == room_db.id
            )
            reservations_db = await self.db.fetch_all(reservations_query)

            reservations = [
                {
                    "id": res.id,
                    "user_name": res.user_name,
                    "start_time": res.start_time,
                    "end_time": res.end_time,
                }
                for res in reservations_db
            ]

            rooms.append(MeetingRoom.from_db(room_db, reservations))

        return rooms

    async def create_reservation(
        self, reservation: ReservationCreate, user_id: UUID
    ) -> UUID:
        room = await self.get(reservation.room_id)
        reservation_id = uuid4()

        if not room.add_reservation(
            reservation_id,
            user_id,
            reservation.start_time,
            reservation.end_time,
        ):
            raise ReservationConflictException("Conflito de horário detectado")

        query = ReservationDB.__table__.insert().values(
            id=str(reservation_id),
            room_id=str(reservation.room_id),
            user_id=str(user_id),
            start_time=reservation.start_time,
            end_time=reservation.end_time,
        )
        await self.db.execute(query)

        self.reservation_subject.notify_creation(
            {
                "id": reservation_id,
                "room_id": reservation.room_id,
                "user_id": user_id,
                "start_time": reservation.start_time,
                "end_time": reservation.end_time,
            }
        )

        return reservation_id

    async def delete_reservation(self, reservation_id: UUID) -> bool:
        query = select(ReservationDB).where(ReservationDB.id == str(reservation_id))
        reservation = await self.db.fetch_one(query)

        if not reservation:
            raise ReservationNotFoundException(
                f"Reserva com id {reservation_id} não encontrada"
            )

        room = await self.get(UUID(reservation.room_id))
        room.cancel_reservation(reservation_id)

        delete_query = ReservationDB.__table__.delete().where(
            ReservationDB.id == str(reservation_id)
        )
        await self.db.execute(delete_query)

        self.reservation_subject.notify_cancellation(str(reservation_id))

        return True

    async def get_reservation_by_id(self, reservation_id: UUID) -> Optional[dict]:
        query = select(ReservationDB).where(ReservationDB.id == str(reservation_id))
        reservation = await self.db.fetch_one(query)

        if not reservation:
            raise ReservationNotFoundException(
                f"Reserva com id {reservation_id} não encontrada"
            )

        return {
            "id": UUID(reservation.id),
            "user_id": UUID(reservation.user_id),
            "room_id": UUID(reservation.room_id),
            "start_time": reservation.start_time,
            "end_time": reservation.end_time,
        }
