import asyncio
import logging
import time

from src.clients.deribit import fetch_price
from src.db.db import async_session_maker
from src.repositories.index_price import IndexPriceRepository
from src.celery_app import celery

logger = logging.getLogger("src.tasks.deribit")


@celery.task
def collect_prices():
    """
    Celery-задача, которая запускает асинхронный сбор индексных цен
    (Index Price) BTC и ETH с биржи Deribit
     и сохраняет их в базу данных.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


async def run():
    """
    Открывает асинхронную сессию базы данных, по очереди запрашивает
    цены для btc_usd и eth_usd из внешнего API Deribit и записывает
    их в таблицу index_price с текущим временем.
    """
    async with async_session_maker() as session:
        repository = IndexPriceRepository(session)

        for ticker in ["btc_usd", "eth_usd"]:
            price = await fetch_price(ticker)
            await repository.add_one(
                {"ticker": ticker, "price": price, "timestamp": int(time.time())}
            )
