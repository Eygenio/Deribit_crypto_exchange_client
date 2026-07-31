import asyncio
import logging
import time

from celery import Celery

from src.clients.deribit import fetch_price
from src.config.settings import settings
from src.db.db import async_session_factory
from src.domain.entities import IndexPrice
from src.infrastructure.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)

celery = Celery(
    "worker",
    broker=settings.broker.url,
    backend=settings.broker.result_backend,
    include=["src.tasks.deribit"],
)

celery.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "src.tasks.deribit.collect_prices",
        "schedule": 60.0,
    }
}


@celery.task
def collect_prices() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


async def run() -> None:
    async with async_session_factory() as session:
        uow = UnitOfWork(session)
        try:
            for ticker in ("btc_usd", "eth_usd"):
                price = await fetch_price(ticker)
                entity = IndexPrice(
                    ticker=ticker,
                    price=price,
                    timestamp=int(time.time()),
                )
                await uow.prices.add(entity)
            await uow.commit()
            logger.info("Prices collected successfully")
        except Exception:
            await uow.rollback()
            logger.exception("Failed to collect prices")
            raise
