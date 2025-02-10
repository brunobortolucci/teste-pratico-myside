from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from domain.models import (
    ReservationCreate,
)
from domain.exceptions import (
    RoomNotFoundException,
    ReservationNotFoundException,
    ReservationConflictException,
)
from infrastructure.repositories import RoomRepository
from infrastructure.database import database

router = APIRouter()
room_repository = RoomRepository(database=database)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova reserva",
    response_description="Reserva criada com sucesso",
)
async def create_reservation(reservation: ReservationCreate) -> dict:
    """
    Cria uma nova reserva de sala com as seguintes informações:
    - **room_id**: ID da sala
    - **user_name**: Nome do usuário
    - **start_time**: Data/hora de início
    - **end_time**: Data/hora de término
    """
    try:
        reservation_id = await room_repository.create_reservation(reservation)
        return {
            "id": reservation_id,
            "room_id": reservation.room_id,
            "user_name": reservation.user_name,
            "start_time": reservation.start_time,
            "end_time": reservation.end_time,
        }
    except RoomNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReservationConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancelar reserva",
    response_description="Reserva cancelada com sucesso",
)
async def delete_reservation(reservation_id: UUID) -> None:
    """
    Cancela uma reserva existente
    """
    try:
        await room_repository.delete_reservation(reservation_id)
    except ReservationNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
