from fastapi import FastAPI
from api.routes import main_router
from domain.exceptions import DomainException
from fastapi import HTTPException, status
from infrastructure.database import database

app = FastAPI(
    title="Sistema de Gerenciamento de Salas de Reunião",
    description="API para gerenciamento de salas de reunião e suas reservas",
    version="1.0.0",
)

app.include_router(main_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.exception_handler(DomainException)
async def domain_exception_handler(request, exc: DomainException):
    """
    Manipulador global para exceções do domínio não tratadas especificamente
    """
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Erro interno: {str(exc)}",
    )


@app.middleware("http")
async def log_requests(request, call_next):
    """
    Middleware para logging de requisições (exemplo)
    """
    response = await call_next(request)
    return response
