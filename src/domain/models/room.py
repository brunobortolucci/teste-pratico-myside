from uuid import UUID
from pydantic import BaseModel, field_validator


class RoomCreate(BaseModel):
    name: str
    capacity: int
    location: str

    @field_validator("capacity")
    def validate_capacity(cls, value: int):
        if value <= 0:
            raise ValueError("A capacidade da sala deve ser maior que 0")
        return value


class RoomResponse(RoomCreate):
    id: UUID
    name: str
    capacity: int
    location: str

    class Config:
        from_attributes = True
