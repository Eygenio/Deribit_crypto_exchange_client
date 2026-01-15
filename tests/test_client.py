import pytest
from httpx import AsyncClient
from src.app import app

@pytest.mark.asyncio
async def test_last_price(client):
    r = await client.get("/api/price/last?ticker=btc_usd")
    assert r.status_code == 200