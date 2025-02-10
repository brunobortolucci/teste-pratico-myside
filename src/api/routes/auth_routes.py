from infrastructure.security import (
    create_access_token,
    verify_password,
)
from domain.models import UserCreate
from infrastructure.database import database
from fastapi import APIRouter, HTTPException, status
from infrastructure.repositories import UserRepository

router = APIRouter()
user_repository = UserRepository(database=database)


@router.post(
    "/token",
    summary="Gerar token de acesso",
    response_description="Token gerado com sucesso",
)
async def login(user: UserCreate) -> dict:
    """
    Gera um token de acesso para o usuário com as credenciais fornecidas
    - **username**: Nome de usuário
    - **password**: Senha
    """
    credentials = await user_repository.get_by_username(user.username)
    if not credentials or not verify_password(user.password, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username, "user_id": credentials.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/register",
    summary="Registrar novo usuário",
    response_description="Usuário registrado com sucesso",
)
async def register(user: UserCreate) -> dict:
    """
    Registra um novo usuário com as credenciais fornecidas
    - **username**: Nome de usuário
    - **password**: Senha
    """
    user_id = await user_repository.create(
        username=user.username, password=user.password
    )
    return {"id": user_id, "username": user.username}
