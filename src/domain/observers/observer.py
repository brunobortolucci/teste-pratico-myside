from typing import List
from abc import ABC, abstractmethod
from domain.models import Reservation


class ReservationObserver(ABC):
    @abstractmethod
    def notify(self, reservation: Reservation):
        pass


class ReservationSubject(ABC):
    def __init__(self):
        self.observers = List[ReservationObserver] = []

    def attach(self, observer: ReservationObserver):
        self.observers.append(observer)

    def notify_all(self, reservation: Reservation):
        for observer in self.observers:
            observer.notify(reservation)
