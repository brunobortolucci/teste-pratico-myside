import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from src.domain.models import ReservationCreate, RoomCreate
from pydantic import ValidationError


def test_valid_room_creation():
    room_data = {"name": "Sala de Reunião A", "capacity": 10, "location": "2º Andar"}
    room = RoomCreate(**room_data)
    assert room.name == room_data["name"]
    assert room.capacity == room_data["capacity"]
    assert room.location == room_data["location"]


def test_invalid_room_capacity():
    room_data = {
        "name": "Sala de Reunião B",
        "capacity": 0,
        "location": "3º Andar",
    }
    with pytest.raises(ValidationError):
        RoomCreate(**room_data)


def test_valid_reservation_creation():
    now = datetime.now()
    reservation_data = {
        "room_id": uuid4(),
        "start_time": now + timedelta(hours=1),
        "end_time": now + timedelta(hours=2),
    }
    reservation = ReservationCreate(**reservation_data)
    assert reservation.room_id == reservation_data["room_id"]
    assert reservation.start_time == reservation_data["start_time"]
    assert reservation.end_time == reservation_data["end_time"]


def test_invalid_reservation_times():
    now = datetime.now()
    reservation_data = {
        "room_id": uuid4(),
        "start_time": now + timedelta(hours=2),
        "end_time": now + timedelta(hours=1),
    }
    with pytest.raises(ValidationError):
        ReservationCreate(**reservation_data)
