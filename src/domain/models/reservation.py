from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, model_validator


class ReservationCreate(BaseModel):
    room_id: UUID
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_times(self) -> "ReservationCreate":
        if self.start_time < datetime.now():
            raise ValueError("Data de início não pode ser menor que a data atual")
        if self.end_time <= self.start_time:
            raise ValueError("Data de fim deve ser maior que a data de início")
        return self


class ReservationResponse(ReservationCreate):
    id: UUID
