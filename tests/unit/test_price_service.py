from unittest.mock import AsyncMock

import pytest

from src.application.services.price_service import PriceService
from src.domain.entities import IndexPrice


@pytest.fixture
def mock_uow() -> AsyncMock:
    uow = AsyncMock()
    uow.prices = AsyncMock()
    return uow


@pytest.mark.asyncio
async def test_get_last(mock_uow: AsyncMock) -> None:
    service = PriceService(mock_uow)
    mock_uow.prices.get_last.return_value = IndexPrice(ticker="btc_usd", price=50000, timestamp=100)
    result = await service.get_last("btc_usd")
    assert result is not None
    assert result.price == 50000
    mock_uow.prices.get_last.assert_called_once_with("btc_usd")


@pytest.mark.asyncio
async def test_get_all(mock_uow: AsyncMock) -> None:
    service = PriceService(mock_uow)
    mock_uow.prices.get_all.return_value = [
        IndexPrice(ticker="btc_usd", price=50000, timestamp=100)
    ]
    result = await service.get_all("btc_usd", page=1)
    assert len(result) == 1
    mock_uow.prices.get_all.assert_called_once_with("btc_usd", 0, 1440)


@pytest.mark.asyncio
async def test_get_by_date(mock_uow: AsyncMock) -> None:
    service = PriceService(mock_uow)
    mock_uow.prices.get_by_date.return_value = []
    result = await service.get_by_date("btc_usd", 100, 200, page=1)
    assert result == []
    mock_uow.prices.get_by_date.assert_called_once_with("btc_usd", 100, 200, 0, 1440)
