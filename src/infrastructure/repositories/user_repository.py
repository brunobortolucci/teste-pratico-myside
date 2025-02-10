from typing import Optional
from uuid import uuid4, UUID
from databases import Database
from infrastructure.models import UserDB
from infrastructure.security import hash_password


class UserRepository:
    def __init__(self, database: Database):
        self.db = database

    async def get_user_by_id(self, user_id: UUID) -> Optional[dict]:
        query = UserDB.__table__.select().where(UserDB.id == str(user_id))
        user_db = await self.db.fetch_one(query)
        if user_db:
            return {
                "id": UUID(user_db["id"]),
                "username": user_db["username"],
            }
        return None

    async def get_by_username(self, username: str) -> UserDB:
        query = UserDB.__table__.select().where(UserDB.username == username)
        user = await self.db.fetch_one(query)
        return user

    async def create(self, username: str, password: str) -> int:
        hashed_password = hash_password(password)
        user_id = uuid4()
        query = UserDB.__table__.insert().values(
            id=str(user_id), username=username, password=hashed_password
        )
        user_id = await self.db.execute(query)
        return user_id
