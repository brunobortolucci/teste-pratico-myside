from datetime import datetime
from .state import RoomState
from typing import TYPE_CHECKING

from .available import AvailableState
from .unavailable import UnavailableState

if TYPE_CHECKING:
    from .available import AvailableState
    from .unavailable import UnavailableState


class PartiallyAvailableState(RoomState):
    def reserve(self, start_time: datetime, end_time: datetime) -> bool:
        if self.check_availability(start_time, end_time):
            has_others = self.room.has_available_period(start_time, end_time)
            if not has_others:
                self.room.state = UnavailableState(self.room)
            return True
        return False

    def cancel(self, start_time: datetime, end_time: datetime) -> bool:
        if len(self.room.reservations) <= 1:
            self.room.state = AvailableState(self.room)
        return True

    def check_availability(self, start_time: datetime, end_time: datetime) -> bool:
        return self.room.is_period_available(start_time, end_time)
