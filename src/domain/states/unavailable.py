from datetime import datetime
from .state import RoomState


class UnavailableState(RoomState):
    def check_availability(self, start_time: datetime, end_time: datetime) -> bool:
        return False
