from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepository:
    """Базовый класс с CRUD операций для SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        # инициализация класса с сессиями базы данных
        self.session = session

    async def add_one(self, data: dict):
        """Добавление одной записи без возврата результата."""
        statement = insert(self.model).values(**data)

        await self.session.execute(statement)
        await self.session.commit()

    async def get_last(self, ticker: str):
        """Получение последней записи."""
        statement = (
            select(self.model)
            .where(self.model.ticker == ticker)
            .order_by(self.model.timestamp.desc())
            .limit(1)
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_all(self, ticker: str, offset: int = 0, limit: int = 100):
        """Получение всех записей с поддержкой пагинации."""
        statement = (
            select(self.model)
            .where(self.model.ticker == ticker)
            .order_by(self.model.timestamp.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_by_date(
            self,
            ticker: str,
            from_ts: int,
            to_ts: int,
            offset: int = 0,
            limit: int = 100
    ):
        """Получение записей с фильтром по дате, а также пагинации."""
        statement = (
            select(self.model)
            .where(
                self.model.ticker == ticker,
                self.model.timestamp.between(from_ts, to_ts),
            )
            .order_by(self.model.timestamp.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()
