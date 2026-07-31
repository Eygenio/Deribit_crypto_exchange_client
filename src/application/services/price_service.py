import logging

from src.application.constants import OFFSET, PAGE_SIZE
from src.domain.entities import IndexPrice
from src.infrastructure.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


class PriceService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def get_last(self, ticker: str) -> IndexPrice | None:
        logger.info("Getting last price for %s", ticker)
        return await self.uow.prices.get_last(ticker)

    async def get_all(
        self,
        ticker: str,
        page: int,
        page_size: int = PAGE_SIZE,
    ) -> list[IndexPrice]:
        logger.info("Getting all prices for %s, page %d", ticker, page)
        offset = (page - OFFSET) * page_size
        return await self.uow.prices.get_all(ticker, offset, page_size)

    async def get_by_date(
        self,
        ticker: str,
        from_ts: int,
        to_ts: int,
        page: int,
        page_size: int = PAGE_SIZE,
    ) -> list[IndexPrice]:
        logger.info("Getting prices for %s from %d to %d, page %d", ticker, from_ts, to_ts, page)
        offset = (page - OFFSET) * page_size
        return await self.uow.prices.get_by_date(ticker, from_ts, to_ts, offset, page_size)
