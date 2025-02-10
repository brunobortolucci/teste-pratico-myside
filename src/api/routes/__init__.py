from fastapi import APIRouter

from .rooms_routes import router as rooms_router
from .reservations_routes import router as reservations_router
from .auth_routes import router as auth_router

reservations_router.include_in_openapi = True
reservations_router.swagger_extra = {
    "security": [{"BearerAuth": []}],
    "responses": {
        401: {"description": "Unauthorized - Token inválido ou não fornecido"}
    },
}

main_router = APIRouter()
main_router.include_router(rooms_router, prefix="/rooms", tags=["rooms"])
main_router.include_router(
    reservations_router, prefix="/reservation", tags=["reservations"]
)
