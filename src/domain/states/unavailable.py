from datetime import datetime
from .state import RoomState
from .partially_available import PartiallyAvailableState


class UnavailableState(RoomState):
    def reserve(self, start_time: datetime, end_time: datetime) -> bool:
        return False

    def cancel(self, start_time: datetime, end_time: datetime) -> bool:
        self.room.state = PartiallyAvailableState(self.room)
        return True

    def check_availability(self, start_time: datetime, end_time: datetime) -> bool:
        return self.room.is_period_available(start_time, end_time)
