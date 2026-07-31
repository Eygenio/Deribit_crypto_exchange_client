from collections.abc import AsyncGenerator

from fastapi import Depends

from src.application.services.price_service import PriceService
from src.db.db import async_session_factory
from src.infrastructure.unit_of_work import UnitOfWork


async def get_uow() -> AsyncGenerator[UnitOfWork]:
    async with async_session_factory() as session:
        yield UnitOfWork(session)


async def get_price_service(
    uow: UnitOfWork = Depends(get_uow),
) -> PriceService:
    return PriceService(uow)
