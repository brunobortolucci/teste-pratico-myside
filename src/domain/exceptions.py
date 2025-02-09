class DomainException(Exception):
    """Exceção base para erros do domínio"""

    pass


class RoomNotFoundException(DomainException):
    """Exceção para quando uma sala não é encontrada"""

    pass


class ReservationNotFoundException(DomainException):
    """Exceção para quando uma reserva não é encontrada"""

    pass


class ReservationConflictException(DomainException):
    """Exceção para conflitos de reserva"""

    pass
