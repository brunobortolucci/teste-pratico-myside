from typing import List, Dict, Optional
from uuid import UUID, uuid4
from datetime import datetime
from ..states.available import AvailableState
from ..exceptions import ReservationNotFoundException


class MeetingRoom:
    def __init__(self, name: str, capacity: int, location: str):
        self.id = uuid4()
        self.name = name
        self.capacity = capacity
        self.location = location
        self.reservations: List[Dict] = []
        self.state = AvailableState(self)

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
        self, user_name: str, start_time: datetime, end_time: datetime
    ) -> bool:
        if not self.state.check_availability(start_time, end_time):
            return False

        reservation = {
            "id": uuid4(),
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
