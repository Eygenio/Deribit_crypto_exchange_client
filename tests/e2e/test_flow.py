import pytest
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models.index_price import IndexPriceOrm

fake = Faker()


@pytest.mark.asyncio
async def test_full_flow(client: AsyncClient, test_session: AsyncSession) -> None:
    resp = await client.get("/api/price/last?ticker=btc_usd")
    assert resp.json() is None

    price = fake.pyfloat(positive=True, min_value=100, max_value=100000)
    ts = fake.random_int(min=1, max=999999999)

    test_session.add(IndexPriceOrm(ticker="btc_usd", price=price, timestamp=ts))
    await test_session.commit()

    resp = await client.get("/api/price/last?ticker=btc_usd")
    assert resp.json()["price"] == price
