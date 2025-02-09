from uuid import UUID
from typing import Dict, List, Optional
from domain.entities import MeetingRoom
from domain.models import ReservationCreate
from domain.exceptions import (
    RoomNotFoundException,
    ReservationNotFoundException,
    ReservationConflictException,
)


class RoomRepository:
    def __init__(self):
        self.rooms: Dict[UUID, MeetingRoom] = {}

    def add(self, room: MeetingRoom) -> None:
        self.rooms[room.id] = room

    def get(self, room_id: UUID) -> Optional[MeetingRoom]:
        room = self.rooms.get(room_id)
        if not room:
            raise RoomNotFoundException(f"Sala com id {room_id} não encontrada")
        return room

    def get_all(self) -> List[MeetingRoom]:
        return list(self.rooms.values())

    def create_reservation(self, reservation: ReservationCreate) -> UUID:
        room = self.get(reservation.room_id)
        success = room.add_reservation(
            reservation.user_name, reservation.start_time, reservation.end_time
        )
        if not success:
            raise ReservationConflictException(
                "Conflito de horário, a sala já está reservada"
            )

        return room.reservations[-1]["id"]

    def delete_reservation(self, reservation_id: UUID) -> bool:
        for room in self.rooms.values():
            try:
                return room.cancel_reservation(reservation_id)
            except ReservationNotFoundException:
                continue

        raise ReservationNotFoundException(
            f"Reserva com id {reservation_id} não encontrada"
        )
