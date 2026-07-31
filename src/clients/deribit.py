import logging

import aiohttp

from src.clients.constants import DERIBIT_URL

logger = logging.getLogger(__name__)


async def fetch_price(ticker: str) -> float:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                DERIBIT_URL,
                params={"index_name": ticker},
            ) as response:
                data = await response.json()
                return float(data["result"]["index_price"])
    except Exception:
        logger.exception("Failed to fetch price for %s", ticker)
        raise
