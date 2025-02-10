from fastapi import FastAPI
from api.routes import main_router, auth_router
from fastapi import HTTPException, status
from fastapi.openapi.utils import get_openapi
from domain.exceptions import DomainException
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.database import database

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Sistema de Gerenciamento de Salas de Reunião",
        description="API para gerenciamento de salas de reunião e suas reservas",
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Insira seu token JWT aqui",
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.openapi = custom_openapi

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(main_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.exception_handler(DomainException)
async def domain_exception_handler(request, exc: DomainException):
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Erro interno: {str(exc)}",
    )
