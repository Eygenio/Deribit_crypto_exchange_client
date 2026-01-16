import pytest

@pytest.mark.asyncio
async def test_last_price(client):
    # no data
    result = await client.get("/api/price/last?ticker=btc_usd")
    assert result.status_code == 200
    assert result.json() is None

@pytest.mark.asyncio
async def test_insert_and_get(client, session):
    from src.models.index_price import IndexPriceOrm

    session.add(IndexPriceOrm(ticker="btc_usd", price=50000, timestamp=100))
    session.add(IndexPriceOrm(ticker="btc_usd", price=51000, timestamp=200))
    await session.commit()

    result = await client.get("/api/price/last?ticker=btc_usd")
    data = result.json()

    assert data["price"] == 51000
    assert data["timestamp"] == 200

@pytest.mark.asyncio
async def test_by_date(client, session):
    from src.models.index_price import IndexPriceOrm

    session.add_all([
        IndexPriceOrm(ticker="eth_usd", price=1000, timestamp=100),
        IndexPriceOrm(ticker="eth_usd", price=1100, timestamp=200),
        IndexPriceOrm(ticker="eth_usd", price=1200, timestamp=300),
    ])
    await session.commit()

    result = await client.get("/api/price/by-date?ticker=eth_usd&from_ts=150&to_ts=250")
    data = result.json()

    assert len(data) == 1
    assert data[0]["price"] == 1100
