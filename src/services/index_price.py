from src.config.base import Config


class IndexPriceService:
    """Сервис для управления индексных цен."""

    def __init__(self, repository):
        self.repository = repository

    async def get_all(self, ticker: str, page: int):
        """Получение списка индексных цен по ticker."""
        offset = (page - 1) * Config.PAGE_SIZE
        return await self.repository.get_all(ticker, offset, Config.PAGE_SIZE)

    async def get_last(self, ticker: str):
        """Получение последнего индексных цен по ticker."""
        return await self.repository.get_last(ticker)

    async def get_by_date(self, ticker: str, from_ts: int, to_ts: int, page: int):
        """Получение списка индексных цен по ticker с фильтрацией по дате."""
        offset = (page - 1) * Config.PAGE_SIZE
        return await self.repository.get_by_date(
            ticker, from_ts, to_ts, offset, Config.PAGE_SIZE
        )
