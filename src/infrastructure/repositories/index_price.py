from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import IndexPrice
from src.domain.repositories import IPriceRepository
from src.infrastructure.models.index_price import IndexPriceOrm


class PriceRepository(IPriceRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(orm: IndexPriceOrm) -> IndexPrice:
        return IndexPrice(
            id=orm.id,
            ticker=orm.ticker,
            price=orm.price,
            timestamp=orm.timestamp,
        )

    async def add(self, price: IndexPrice) -> None:
        orm = IndexPriceOrm(
            ticker=price.ticker,
            price=price.price,
            timestamp=price.timestamp,
        )
        self._session.add(orm)
        await self._session.flush()

    async def get_last(self, ticker: str) -> IndexPrice | None:
        statement = (
            select(IndexPriceOrm)
            .where(IndexPriceOrm.ticker == ticker)
            .order_by(IndexPriceOrm.timestamp.desc())
            .limit(1)
        )
        result = await self._session.execute(statement)
        orm = result.scalar_one_or_none()
        return self._to_domain(orm) if orm else None

    async def get_all(
        self,
        ticker: str,
        offset: int,
        limit: int,
    ) -> list[IndexPrice]:
        statement = (
            select(IndexPriceOrm)
            .where(IndexPriceOrm.ticker == ticker)
            .order_by(IndexPriceOrm.timestamp.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.execute(statement)
        return [self._to_domain(row) for row in result.scalars().all()]

    async def get_by_date(
        self,
        ticker: str,
        from_ts: int,
        to_ts: int,
        offset: int,
        limit: int,
    ) -> list[IndexPrice]:
        statement = (
            select(IndexPriceOrm)
            .where(
                IndexPriceOrm.ticker == ticker,
                IndexPriceOrm.timestamp.between(from_ts, to_ts),
            )
            .order_by(IndexPriceOrm.timestamp.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.execute(statement)
        return [self._to_domain(row) for row in result.scalars().all()]
