from datetime import datetime
from .state import RoomState


class AvailableState(RoomState):
    def check_availability(self, start_time: datetime, end_time: datetime) -> bool:
        return self.room.is_period_available(start_time, end_time)
