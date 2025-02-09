from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities import MeetingRoom


class RoomState(ABC):
    def __init__(self, room: "MeetingRoom"):
        self.room = room

    @abstractmethod
    def reserve(self, start_time: datetime, end_time: datetime) -> bool:
        pass

    @abstractmethod
    def cancel(self, start_time: datetime, end_time: datetime) -> bool:
        pass

    @abstractmethod
    def check_availability(self, start_time: datetime, end_time: datetime) -> bool:
        pass
