from abc import ABC, abstractmethod

from src.domain.entities import IndexPrice


class IPriceRepository(ABC):
    @abstractmethod
    async def add(self, price: IndexPrice) -> None:
        pass

    @abstractmethod
    async def get_last(self, ticker: str) -> IndexPrice | None:
        pass

    @abstractmethod
    async def get_all(
        self,
        ticker: str,
        offset: int,
        limit: int,
    ) -> list[IndexPrice]:
        pass

    @abstractmethod
    async def get_by_date(
        self,
        ticker: str,
        from_ts: int,
        to_ts: int,
        offset: int,
        limit: int,
    ) -> list[IndexPrice]:
        pass
