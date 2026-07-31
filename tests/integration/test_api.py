import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models.index_price import IndexPriceOrm

fake = Faker()


@pytest.mark.asyncio
async def test_last_price_empty(client: AsyncClient) -> None:
    response = await client.get("/api/price/last?ticker=btc_usd")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is None


@pytest.mark.asyncio
async def test_insert_and_get(client: AsyncClient, test_session: AsyncSession) -> None:
    price1 = fake.pyfloat(positive=True, min_value=100, max_value=100000)
    price2 = fake.pyfloat(positive=True, min_value=100, max_value=100000)
    ts1 = 100
    ts2 = 200

    test_session.add_all(
        [
            IndexPriceOrm(ticker="btc_usd", price=price1, timestamp=ts1),
            IndexPriceOrm(ticker="btc_usd", price=price2, timestamp=ts2),
        ]
    )
    await test_session.commit()

    response = await client.get("/api/price/last?ticker=btc_usd")
    data = response.json()
    assert data["price"] == price2
    assert data["timestamp"] == ts2


@pytest.mark.asyncio
async def test_by_date(client: AsyncClient, test_session: AsyncSession) -> None:
    price1 = fake.pyfloat(positive=True, min_value=1, max_value=1000)
    price2 = fake.pyfloat(positive=True, min_value=1, max_value=1000)
    price3 = fake.pyfloat(positive=True, min_value=1, max_value=1000)
    ts1 = 100
    ts2 = 200
    ts3 = 300

    test_session.add_all(
        [
            IndexPriceOrm(ticker="eth_usd", price=price1, timestamp=ts1),
            IndexPriceOrm(ticker="eth_usd", price=price2, timestamp=ts2),
            IndexPriceOrm(ticker="eth_usd", price=price3, timestamp=ts3),
        ]
    )
    await test_session.commit()

    response = await client.get("/api/price/by-date?ticker=eth_usd&from_ts=150&to_ts=250")
    data = response.json()
    assert len(data) == 1
    assert data[0]["price"] == price2
