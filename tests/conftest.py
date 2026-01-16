import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.models.base import ModelBase
from src.db.db import get_async_session
from src.app import app

TEST_DB = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def engine():  # без scope="session"
    engine = create_async_engine(TEST_DB)
    async with engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as s:
        yield s


@pytest_asyncio.fixture
async def client(session):
    async def override():
        yield session

    app.dependency_overrides[get_async_session] = override

    transport = ASGITransport(app=app)  # вот так подключаем FastAPI
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
