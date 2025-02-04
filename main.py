import uuid
from datetime import datetime
from pydantic import BaseModel, field_validator
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

class Room(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    name: str
    capacity: int
    location: str

    @field_validator("capacity")
    def check_capacity(cls, v):
        # Essa validação está ok, mas necessário validar um melhor retorno para o frontend
        if v < 1:
            raise ValueError("A capacidade da sala deve ser maior que 0")
        return v

class Reservation(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    room_id: uuid.UUID
    user_name: str
    start_time: datetime
    end_time: datetime

    @field_validator("start_time")
    def check_dates(cls, v):
        # Melhorar a lógica pois precisamos considerar o formato da data (E também não está funcional)
        if v < datetime.now():
            raise ValueError("A data de início da reserva não pode ser menor que a data atual")
        return v

    @field_validator("end_time")
    def check_end_time(cls, v):
        # Essa condição abaixo ainda não foi validada
        if v < cls.start_time:
            raise ValueError("A data de fim da reserva não pode ser menor que a data de início")
        return v

rooms = []
meetings = []

@app.post("/rooms", status_code=status.HTTP_201_CREATED)
async def create_room(room: Room):
    try:
      rooms.append(room)
      return f"Sala {room.name}, com capacidade para {room.capacity} pessoas localizada em {room.location} foi criada com sucesso!"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/rooms", status_code=status.HTTP_200_OK)
async def get_rooms():
    return rooms if rooms else "Nenhuma sala encontrada!"

@app.get("/rooms/{id}/availability", status_code=status.HTTP_200_OK)
async def get_room_availability(id: uuid.UUID):
    # Aqui é necessário validar se a sala não está reservada no momento da requisição
    for room in rooms:
        if room.id == id:
            return room
        else:
            return "Sala não encontrada!"

@app.post("/reservations", status_code=status.HTTP_201_CREATED)
async def create_reservation(reservation: Reservation):
    if reservation.room_id not in [room.id for room in rooms]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A sala informada não foi encontrada!")
    meetings.append(reservation)
    return f"Reserva para a sala {reservation.room_id} foi criada com sucesso!"

@app.delete("/reservations/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation():
    if not meetings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma reserva encontrada!")    
    return "Ok!"

@app.get("/rooms/{id}/reservations", status_code=status.HTTP_200_OK)
async def get_reservations(id: uuid.UUID):
    if not meetings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma reserva encontrada!")
    for meeting in meetings:
        if meeting.room_id == id:
            return meeting
        else:
            return "Nenhuma reserva encontrada para esta sala!"