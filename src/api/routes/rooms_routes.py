from uuid import UUID
from typing import List
from datetime import datetime
from fastapi import APIRouter, Query, HTTPException, status
from domain.entities import MeetingRoom
from domain.models import (
    RoomCreate,
    RoomResponse,
)
from domain.exceptions import (
    RoomNotFoundException,
)
from infrastructure.repositories import RoomRepository
from infrastructure.database import database

router = APIRouter()
room_repository = RoomRepository(database=database)


@router.post(
    "/",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova sala",
    response_description="Sala criada com sucesso",
)
async def create_room(room_data: RoomCreate) -> MeetingRoom:
    """
    Cria uma nova sala de reunião com as seguintes informações:
    - **name**: Nome da sala
    - **capacity**: Capacidade máxima de pessoas
    - **location**: Localização da sala
    """
    try:
        new_room = MeetingRoom(
            name=room_data.name,
            capacity=room_data.capacity,
            location=room_data.location,
        )
        await room_repository.add(new_room)
        return new_room
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/",
    response_model=List[RoomResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todas as salas",
    response_description="Lista de salas retornadas com sucesso",
)
async def list_rooms(
    page: int = Query(1, description="Número da página"),
    per_page: int = Query(10, description="Número de itens por página"),
) -> MeetingRoom:
    """Retorna a lista de todas as salas cadastradas"""
    return await room_repository.get_all()


@router.get(
    "/{room_id}/availability",
    status_code=status.HTTP_200_OK,
    summary="Verificar disponibilidade da sala",
    response_description="Status de disponibilidade da sala",
)
async def get_room_availability(
    room_id: UUID,
    start_time: datetime = Query(
        ..., description="Data/hora de início (YYYY-MM-DDTHH:MM:SS)"
    ),
    end_time: datetime = Query(
        ..., description="Data/hora de término (YYYY-MM-DDTHH:MM:SS)"
    ),
) -> dict:
    """
    Verifica a disponibilidade de uma sala para um período específico
    """
    try:
        if end_time <= start_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data de fim deve ser maior que a data de início",
            )

        room = await room_repository.get(room_id)
        is_available = room.check_availability(start_time, end_time)

        return {
            "room_id": room_id,
            "start_time": start_time,
            "end_time": end_time,
            "is_available": is_available,
            "status": "disponível" if is_available else "indisponível",
        }
    except RoomNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{room_id}/reservations",
    status_code=status.HTTP_200_OK,
    summary="Listar reservas da sala",
    response_description="Lista de reservas recuperada com sucesso",
)
async def list_room_reservations(
    room_id: UUID,
    date: datetime | None = Query(
        None, description="Data para filtrar as reservas (YYYY-MM-DD)"
    ),
) -> List[dict]:
    """
    Lista todas as reservas de uma sala, com opção de filtro por data
    """
    try:
        room = await room_repository.get(room_id)
        reservations = room.get_reservations()

        if date:
            reservations = [
                reservation
                for reservation in reservations
                if reservation["start_time"].date() == date.date()
            ]

        return reservations
    except RoomNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
