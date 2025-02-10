import logging
from uuid import UUID
from typing import List
from datetime import datetime
from abc import ABC, abstractmethod

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("reservations.log"),
        logging.StreamHandler(),
    ],
)


class ReservationObserver(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def notify_reservation_created(self, reservation: dict) -> None:
        pass

    @abstractmethod
    def notify_reservation_cancelled(self, reservation_id: str) -> None:
        pass


class LoggingObserver(ReservationObserver):
    def notify_reservation_created(self, reservation: dict) -> None:
        self.logger.info(
            "Reserva criada | "
            + f"Sala: {reservation['room_id']} | "
            + f"Usuário: {reservation['user_id']} | "
            + f"Início: {reservation['start_time']} | "
            + f"Fim: {reservation['end_time']}"
        )

    def notify_reservation_cancelled(self, reservation_id: str) -> None:
        self.logger.info(f"Reserva cancelada | ID: {reservation_id}")


class EmailObserver(ReservationObserver):
    def notify_reservation_created(self, reservation: dict) -> None:
        self.logger.info(
            f"Email enviado | "
            + f"Confirmação de reserva para usuário {reservation['user_id']} | "
            + f"Sala {reservation['room_id']}"
        )

    def notify_reservation_cancelled(self, reservation_id: str) -> None:
        self.logger.info(
            f"Email enviado | "
            + f"Notificação de cancelamento da reserva {reservation_id}"
        )


class ConflictObserver(ReservationObserver):
    def notify_reservation_created(self, reservation: dict) -> None:
        self.logger.info(
            f"Verificando conflitos | "
            + f"Sala: {reservation['room_id']} | "
            + f"Período: {reservation['start_time']} - {reservation['end_time']}"
        )

    def notify_reservation_cancelled(self, reservation_id: str) -> None:
        self.logger.info(
            f"Verificando impactos do cancelamento | " + f"Reserva: {reservation_id}"
        )

    def notify_conflict_detected(
        self, room_id: UUID, start_time: datetime, end_time: datetime
    ) -> None:
        self.logger.warning(
            f"Conflito detectado | "
            + f"Sala: {room_id} | "
            + f"Período conflitante: {start_time} - {end_time}"
        )


class ReservationSubject:
    def __init__(self):
        self._observers: List[ReservationObserver] = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def attach(self, observer: ReservationObserver) -> None:
        self._observers.append(observer)
        self.logger.debug(f"Observer {observer.__class__.__name__} registrado")

    def detach(self, observer: ReservationObserver) -> None:
        self._observers.remove(observer)
        self.logger.debug(f"Observer {observer.__class__.__name__} removido")

    def notify_creation(self, reservation: dict) -> None:
        for observer in self._observers:
            try:
                observer.notify_reservation_created(reservation)
            except Exception as e:
                self.logger.error(
                    f"Erro ao notificar {observer.__class__.__name__}: {str(e)}"
                )

    def notify_cancellation(self, reservation_id: str) -> None:
        for observer in self._observers:
            try:
                observer.notify_reservation_cancelled(reservation_id)
            except Exception as e:
                self.logger.error(
                    f"Erro ao notificar {observer.__class__.__name__}: {str(e)}"
                )
