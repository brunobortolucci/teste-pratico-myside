from uuid import uuid4, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()


class RoomDB(Base):
    __tablename__ = "rooms"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    location = Column(String(100), nullable=False)


class UserDB(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)


class ReservationDB(Base):
    __tablename__ = "reservations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    room_id = Column(String(36), ForeignKey("rooms.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
