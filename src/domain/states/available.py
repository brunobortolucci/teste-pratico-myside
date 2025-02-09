from datetime import datetime
from .state import RoomState
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .partially_available import PartiallyAvailableState
    from .unavailable import UnavailableState


class AvailableState(RoomState):
    def reserve(self, start_time: datetime, end_time: datetime) -> bool:
        if self.check_availability(start_time, end_time):
            has_others = self.room.has_available_period(start_time, end_time)
            if has_others:
                self.room.state = PartiallyAvailableState(self.room)
            else:
                self.room.state = UnavailableState(self.room)
            return True
        return False

    def cancel(self, start_time: datetime, end_time: datetime) -> bool:
        return False

    def check_availability(self, start_time: datetime, end_time: datetime) -> bool:
        return self.room.is_period_available(start_time, end_time)
