from datetime import datetime, timedelta
from uuid import uuid4
from src.domain.entities import MeetingRoom
from src.domain.states import AvailableState, PartiallyAvailableState, UnavailableState


def test_initial_state():
    room = MeetingRoom(name="Initial State Room", capacity=5, location="Test")
    assert isinstance(room.state, AvailableState)


def test_transition_to_partially_available():
    room = MeetingRoom(name="Transition Room", capacity=5, location="Test")
    now = datetime.now()

    success = room.add_reservation(
        uuid4(), "user1", now + timedelta(hours=1), now + timedelta(hours=2)
    )
    assert success is True
    assert isinstance(room.state, AvailableState)

    success = room.add_reservation(
        uuid4(), "user2", now + timedelta(hours=3), now + timedelta(hours=4)
    )
    assert success is True
    assert isinstance(room.state, PartiallyAvailableState)
    assert len(room.reservations) == 2


def test_transition_to_unavailable():
    room = MeetingRoom(name="Full Room", capacity=5, location="Test")
    now = datetime.now()

    for i in range(16):
        success = room.add_reservation(
            uuid4(),
            f"user{i}",
            now + timedelta(hours=i * 2),
            now + timedelta(hours=(i * 2) + 1),
        )
        assert success is True

    assert isinstance(room.state, UnavailableState)
    assert len(room.reservations) == 16


def test_state_recovery_after_cancellation():
    room = MeetingRoom(name="Cancel Room", capacity=5, location="Test")
    now = datetime.now()

    reservation_ids = []
    for i in range(2):
        res_id = uuid4()
        reservation_ids.append(res_id)
        success = room.add_reservation(
            res_id,
            f"user{i}",
            now + timedelta(hours=i * 2),
            now + timedelta(hours=(i * 2) + 1),
        )
        assert success is True

    assert isinstance(room.state, PartiallyAvailableState)
    assert len(room.reservations) == 2

    room.cancel_reservation(reservation_ids[0])
    assert isinstance(room.state, AvailableState)
    assert len(room.reservations) == 1
