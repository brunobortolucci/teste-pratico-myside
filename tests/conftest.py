import pytest
import asyncio
import sys
from pathlib import Path
from databases import Database
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from infrastructure.models import Base
from main import app

project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.append(str(src_path))


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def database():
    TEST_DATABASE_URL = "sqlite:///test.db"
    db = Database(TEST_DATABASE_URL)

    await db.connect()

    yield db

    await db.disconnect()


@pytest.fixture
async def room_repository(database):
    from infrastructure.repositories import RoomRepository

    return RoomRepository(database)


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client
