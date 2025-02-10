from datetime import datetime
from .state import RoomState


class UnavailableState(RoomState):
    def reserve(self, start_time: datetime, end_time: datetime) -> bool:
        return False

    def cancel(self, start_time: datetime, end_time: datetime) -> bool:
        """
        Importação do estado feito dentro do método de cancelar a reserva
        para evitar problemas de importação circular
        """
        from .partially_available import (
            PartiallyAvailableState,
        )

        self.room.state = PartiallyAvailableState(self.room)
        return True

    def check_availability(self, start_time: datetime, end_time: datetime) -> bool:
        return self.room.is_period_available(start_time, end_time)
