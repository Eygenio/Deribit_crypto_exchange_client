from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.app import app
from src.infrastructure.models.base import ModelBase
from src.infrastructure.unit_of_work import UnitOfWork
from src.presentation.dependencies import get_uow

TEST_DB = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def test_engine() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(TEST_DB)
    async with engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def test_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession]:
    session_factory = async_sessionmaker(test_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    async def override_get_uow() -> AsyncGenerator[UnitOfWork]:
        yield UnitOfWork(test_session)

    app.dependency_overrides[get_uow] = override_get_uow
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.pop(get_uow, None)
