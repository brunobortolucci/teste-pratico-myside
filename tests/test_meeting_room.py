import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from src.domain.entities import MeetingRoom
from src.domain.exceptions import ReservationNotFoundException


def test_meeting_room_creation():
    room = MeetingRoom(name="Test Room", capacity=10, location="Building A")
    assert room.name == "Test Room"
    assert room.capacity == 10
    assert room.location == "Building A"
    assert room.id is not None


def test_room_availability():
    room = MeetingRoom(name="Available Room", capacity=5, location="Building B")
    now = datetime.now()
    future_start = now + timedelta(hours=1)
    future_end = now + timedelta(hours=2)

    assert room.check_availability(future_start, future_end) is True


def test_room_reservation():
    room = MeetingRoom(name="Reservation Room", capacity=5, location="Building C")
    reservation_id = uuid4()
    now = datetime.now()

    start_time = now + timedelta(hours=1)
    end_time = now + timedelta(hours=2)

    result = room.add_reservation(reservation_id, "John Doe", start_time, end_time)
    assert result is True
    assert len(room.reservations) == 1


def test_overlapping_reservation():
    room = MeetingRoom(name="Conflict Room", capacity=5, location="Building D")
    now = datetime.now()

    first_id = uuid4()
    start_time1 = now + timedelta(hours=1)
    end_time1 = now + timedelta(hours=2)

    room.add_reservation(first_id, "User 1", start_time1, end_time1)

    second_id = uuid4()
    overlapping_start = now + timedelta(hours=1, minutes=30)
    overlapping_end = now + timedelta(hours=2, minutes=30)

    result = room.add_reservation(
        second_id, "User 2", overlapping_start, overlapping_end
    )
    assert result is False


def test_cancel_reservation():
    room = MeetingRoom(name="Cancellation Room", capacity=5, location="Building E")
    now = datetime.now()

    reservation_id = uuid4()
    start_time = now + timedelta(hours=1)
    end_time = now + timedelta(hours=2)

    room.add_reservation(reservation_id, "Canceller", start_time, end_time)

    room.cancel_reservation(reservation_id)
    assert len(room.reservations) == 0


def test_cancel_nonexistent_reservation():
    room = MeetingRoom(
        name="Non-Existent Reservation Room", capacity=5, location="Building F"
    )
    non_existent_id = uuid4()

    with pytest.raises(ReservationNotFoundException):
        room.cancel_reservation(non_existent_id)
