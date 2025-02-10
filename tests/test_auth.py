import pytest
from datetime import timedelta
from fastapi import HTTPException
from infrastructure.security import (
    create_access_token,
    verify_password,
    hash_password,
    get_current_user,
)


def test_password_hashing():
    password = "test_password123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_token_creation():
    data = {"sub": "test_user", "user_id": "123"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.asyncio
async def test_token_expiration():
    data = {"sub": "test_user", "user_id": "123"}
    expires = timedelta(minutes=-10)
    expired_token = create_access_token(data, expires)

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(expired_token)

    assert exc_info.value.status_code == 401
    assert "Credenciais inválidas" in str(exc_info.value.detail)
