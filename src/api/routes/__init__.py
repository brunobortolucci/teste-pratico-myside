from fastapi import APIRouter

from .rooms_routes import router as rooms_routes
from .reservations_routes import router as reservations_routes

main_router = APIRouter()
main_router.include_router(rooms_routes, prefix="/rooms", tags=["rooms"])
main_router.include_router(
    reservations_routes, prefix="/reservation", tags=["reservations"]
)
