from typing import List, Dict
from uuid import UUID, uuid4
from datetime import datetime
from ..states import AvailableState, PartiallyAvailableState, UnavailableState
from ..exceptions import ReservationNotFoundException


class MeetingRoom:
    def __init__(self, name: str, capacity: int, location: str):
        self.id = uuid4()
        self.name = name
        self.capacity = capacity
        self.location = location
        self.reservations: List[Dict] = []
        self.state = AvailableState(self)

    @staticmethod
    def from_db(room_db, reservations) -> "MeetingRoom":
        room = MeetingRoom(
            name=room_db.name,
            capacity=room_db.capacity,
            location=room_db.location,
        )
        room.id = room_db.id
        room.reservations = [
            {
                "id": UUID(res["id"]),
                "user_name": res["user_name"],
                "start_time": res["start_time"],
                "end_time": res["end_time"],
            }
            for res in reservations
        ]

        if not reservations:
            room.state = AvailableState(room)
        elif len(reservations) == 1:
            room.state = PartiallyAvailableState(room)
        else:
            room.state = UnavailableState(room)

        return room

    def is_period_available(self, start_time: datetime, end_time: datetime) -> bool:
        return not any(
            reservation["start_time"] < end_time
            and reservation["end_time"] > start_time
            for reservation in self.reservations
        )

    def has_available_period(self, start_time: datetime, end_time: datetime) -> bool:
        for reservation in self.reservations:
            if (
                reservation["start_time"] < end_time
                and reservation["end_time"] > start_time
            ):
                return True
        return len(self.reservations) == 0

    def get_reservations(self) -> List[Dict]:
        return self.reservations

    def add_reservation(
        self,
        reservation_id: UUID,
        user_name: str,
        start_time: datetime,
        end_time: datetime,
    ) -> bool:
        if not self.state.check_availability(start_time, end_time):
            return False

        reservation = {
            "id": reservation_id,
            "user_name": user_name,
            "start_time": start_time,
            "end_time": end_time,
        }
        self.reservations.append(reservation)
        self.state.reserve(start_time, end_time)
        return True

    def cancel_reservation(self, reservation_id: UUID) -> bool:
        reservation = next(
            (
                reservation
                for reservation in self.reservations
                if reservation["id"] == reservation_id
            ),
            None,
        )
        if not reservation:
            raise ReservationNotFoundException(
                f"Reserva com id {reservation_id} não encontrada"
            )

        start_time = reservation["start_time"]
        end_time = reservation["end_time"]
        self.reservations.remove(reservation)
        return self.state.cancel(start_time, end_time)

    def check_availability(self, start_time: datetime, end_time: datetime) -> bool:
        if self.state.check_availability(start_time, end_time):
            return True
        return False
